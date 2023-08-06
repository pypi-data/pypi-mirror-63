#!/usr/bin/python3

import baseconfig
import dns.resolver
import dns.reversename
import logging
import pika
import random
import ssl


class Mqs:
    def __init__(self, app_config, exchange, exit_event):
        self._app_config = app_config
        self._exchange = exchange
        self._exit_event = exit_event
        self._channel = None
        self._log = logging.getLogger("sslmqs")

    def start(self):
        self._instances = self._list_hosts()
        random.shuffle(self._instances)
        self._connect(self._instances.pop())

    def _connect(self, instance):
        self._log.info("Trying to connect to {}...".format(instance))
        parameters = self.generate_instance_params(
            instance, self._app_config, 2)
        self._connection = pika.SelectConnection(
            parameters=parameters,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

        self._connection.ioloop._timer.call_later(2, self.on_timeout)
        self._connection.ioloop.start()

    def on_timeout(self):
        if self._exit_event.is_set():
            self._log.info("Exit event received; closing the connection.")
            try:
                if self._channel:
                    self._channel.close()
            except pika.exceptions.ChannelWrongStateError:
                self._log.debug("Channel already closing.")

            try:
                self._connection.close()
            except pika.exceptions.ConnectionWrongStateError:
                self._log.debug("Connection already closing.")

            self._connection.ioloop.stop()
        else:
            self.on_timeout_custom()
            self._connection.ioloop._timer.call_later(0.02, self.on_timeout)

    def on_connection_open(self, connection):
        self._log.info(
            "Connection to {} opened.".format(connection.params.host))
        self._channel = connection.channel(
            on_open_callback=self.on_channel_open)

        connection._heartbeat_checker._check_interval = 1
        self._instances.append(connection.params.host)

    def on_connection_open_error(self, connection, ex):
        self._log.error("Connection to {} failed: {}".format(
            connection.params.host,
            str(ex) or "reason not specified."))
        self._reopen(connection)

    def on_connection_closed(self, connection, reason):
        self._log.info("Connection to {} closed: {}".format(
            connection.params.host, reason))
        self._reopen(connection)

    def _reopen(self, connection):
        connection.ioloop.stop()
        self._channel = None
        current_instance = connection.params.host

        try:
            instance = self._instances.pop(
                1 if self._instances[0] == current_instance else 0
            )
            self._connect(instance)
        except IndexError:
            self._log.info("No more servers left.")
            self._exit_event.set()

    def _list_hosts(self):
        try:
            _ = self._app_config.mqs_hosts
            has_hosts = True
        except baseconfig.ValueMissingException:
            has_hosts = False

        try:
            domain = self._app_config.mqs_domain
            if has_hosts:
                raise Exception(
                    "One shouldn't configure both the domain and the hosts "
                    "for MQS."
                )

            results = dns.resolver.query("test-mqs", "A")
            return [self._ip_to_instance_name(r.to_text()) for r in results]
        except baseconfig.ValueMissingException:
            return self._app_config.mqs_hosts

    def _ip_to_instance_name(self, ip):
        arpa = dns.reversename.from_address(ip)
        result = dns.resolver.query(arpa, "PTR")
        domain_name = result[0].to_text()[:-1]
        return domain_name[:domain_name.index(".")]

    def on_channel_open(self, channel):
        self._log.info("The channel {} to {} is opened.".format(
            channel.channel_number,
            channel.connection.params.host))
        self.on_channel_open_custom(channel)
        channel.exchange_declare(
            exchange=self._exchange,
            exchange_type="direct",
            callback=self.on_exchange_declare_ok)

    def generate_instance_params(self, instance, config, timeout):
        context = ssl.create_default_context(cafile=config.tls_ca)
        context.load_cert_chain(config.tls_cert, config.tls_key)
        ssl_options = pika.SSLOptions(context, instance)

        return pika.ConnectionParameters(
            host=instance,
            port=config.mqs_port,
            virtual_host=config.mqs_vhost,
            ssl_options=ssl_options,
            credentials=pika.credentials.ExternalCredentials(),
            heartbeat=1,
            socket_timeout=timeout,
            stack_timeout=timeout,
            blocked_connection_timeout=1,
            connection_attempts=1,
            retry_delay=0)
