import logging
import multiprocessing
import pika
import queue
import ssl
import sslmqs


class MqsPublisher:
    def __init__(self, app_config, exchange, routing_key, exit_event):
        self._app_config = app_config
        self._exchange = exchange
        self._routing_key = routing_key
        self._exit_event = exit_event

    def start(self, app_config, messages):
        def parallel(messages_queue, exit_event):
            logger = logging.getLogger("sslmqs")
            try:
                s = MqsPublisherAsync(
                    self._app_config,
                    self._exchange,
                    self._routing_key,
                    exit_event,
                    messages_queue)
                s.start()
            except Exception:
                logger.error("Unhandled exception:", exc_info=True)
                raise

        p = multiprocessing.Process(
            name="sslmqs.publish",
            target=parallel,
            args=(messages, self._exit_event)
        )
        p.start()
        return p


class MqsPublisherAsync(sslmqs.Mqs):
    def __init__(
            self, app_config, exchange, routing_key, exit_event, messages):
        super().__init__(app_config, exchange, exit_event)
        self._routing_key = routing_key
        self._messages = messages
        self._sent_counter = 1
        self._sent = {}

    def on_timeout_custom(self):
        if not self._channel:
            return

        try:
            message = self._messages.get_nowait()
            if message:
                self._log.debug("Publishing {}.".format(message))
                self._sent[self._sent_counter] = message
                self._sent_counter += 1
                self._channel.basic_publish(
                    self._exchange, self._routing_key, message)
        except queue.Empty:
            pass

    def on_channel_open_custom(self, channel):
        self._sent_counter = 1

    def on_exchange_declare_ok(self, frame):
        try:
            self._log.debug("Exchange declared.")
            self._channel.confirm_delivery(self.on_delivery_confirmation)
        except:
            self._log.error("Unhandled exception:", exc_info=True)
            raise

    def on_delivery_confirmation(self, method_frame):
        try:
            key = method_frame.method.delivery_tag
            message = self._sent.pop(key)
            self._log.debug("Confirmed delivery of {}.".format(message))
        except KeyError:
            self._log.warning(
                "Delivery confirmation couldn't find key {}.".format(key))
        except:
            self._log.error("Unhandled exception:", exc_info=True)
            raise
