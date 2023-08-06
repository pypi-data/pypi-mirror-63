import ctypes
import logging
import multiprocessing
import pika
import queue
import ssl
import sslmqs


class MqsSubscriber:
    def __init__(
            self,
            app_config,
            exchange,
            routing_key,
            queue,
            exit_event,
            durable):
        self._app_config = app_config
        self._exchange = exchange
        self._routing_key = routing_key
        self._queue = queue
        self._exit_event = exit_event
        self._durable = durable
        self._additional_routing_keys = multiprocessing.Array(
            ctypes.c_char, 500)

    def listen(self, messages):
        def parallel(messages_queue, exit_event, additional_routing_keys):
            logger = logging.getLogger("sslmqs")
            try:
                s = MqsSubscriberAsync(
                    self._app_config,
                    self._exchange,
                    self._routing_key,
                    self._queue,
                    messages_queue,
                    exit_event,
                    self._durable,
                    additional_routing_keys)

                s.start()
            except Exception:
                logger.error("listen failed.", exc_info=True)
                raise

        logger = logging.getLogger("sslmqs")
        p = multiprocessing.Process(
            name="sslmqs.listen",
            target=parallel,
            args=(messages, self._exit_event, self._additional_routing_keys))
        p.start()

        return p

    def add_routing(self, queue_name, routing_key):
        current = self._additional_routing_keys.value.decode()
        if current != "" and current.startswith("ok:"):
            raise Exception("A routing key is being already added.")

        self._additional_routing_keys.value = "add:{}::{}".format(
            queue_name, routing_key).encode()


class MqsSubscriberAsync(sslmqs.Mqs):
    def __init__(
            self,
            app_config,
            exchange,
            routing_key,
            queue,
            messages_queue,
            exit_event,
            durable,
            additional_routing_keys):
        super().__init__(app_config, exchange, exit_event)
        self._routing_key = routing_key
        self._queue = queue
        self._messages_queue = messages_queue
        self._durable = durable

        # The shared string is used to add routing keys on the fly.
        self._additional_routing_keys = additional_routing_keys

    def on_timeout_custom(self):
        self._add_routing_keys()

    def _add_routing_keys(self):
        additional = self._additional_routing_keys.value.decode()
        if additional.startswith("add:"):
            queue_name, routing_key = additional[4:].split("::")

            def local_on_bind_ok(frame):
                self._additional_routing_keys.value = "ok:{}::{}".format(
                    queue_name, routing_key).encode()

            if not self._channel:
                self._additional_routing_keys.value = "err:{}::{}::{}".format(
                    queue_name,
                    routing_key,
                    "The channel is not initialized yet.").encode()

            self._channel.queue_bind(
                queue_name,
                self._exchange,
                routing_key=routing_key,
                callback=local_on_bind_ok)

    def on_channel_open_custom(self, channel):
        pass

    def on_exchange_declare_ok(self, frame):
        self._log.debug("Exchange declared.")
        self._channel.queue_declare(
            queue=self._queue,
            callback=self.on_queue_declare_ok,
            auto_delete=not self._durable,
            durable=self._durable)

    def on_queue_declare_ok(self, frame):
        self._log.debug("Queue declared.")
        self._channel.queue_bind(
            self._queue,
            self._exchange,
            routing_key=self._routing_key,
            callback=self.on_bind_ok)

    def on_bind_ok(self, frame):
        self._log.debug("The queue is bound to the exchange.")
        self._channel.basic_qos(
            prefetch_count=1,
            callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, frame):
        self._log.debug("The QOS is set.")
        self._channel.basic_consume(self._queue, self.on_message)

    def on_message(self, channel, basic_deliver, properties, body):
        self._log.debug(
            "Message {} received.".format(basic_deliver.delivery_tag))
        channel.basic_ack(basic_deliver.delivery_tag)
        self._messages_queue.put(body)
