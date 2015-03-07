# -*- coding: utf-8 -*-

"""
psitats.queue
~~~~~~~~~~~~~

Wrapper around pika

"""

import pika
from psistats import exceptions
from urlparse import urlparse

class Queue():
    """A basic wrapper around pika

    Exposes only the functionlity needed by Psistats
    in a neat convenient class.

    :param url: URL (amqp scheme) to the RabbitMQ server
    :param queue_config: Dict containing the queue configuration. Queue
        configuration needs the following: name, durable, exclusive,
        autodelete, and ttl
    :param exchange_config: Dict containing the exchange configuration.
        Exchange configuration needs the following: name, type, durable,
        and autodelete
    """

    def __init__(self, url, queue_config, exchange_config):

        self.url = url
        self.queue_config = queue_config
        self.exchange_config = exchange_config

        self._msg_properties = pika.spec.BasicProperties(
            content_type="application/json",
            content_encoding="utf-8"
        )

        self._connection = None
        self._channel = None

        try:
            self._params = pika.URLParameters(url)
        except Exception as e:
            raise exceptions.ConfigException("Invalid URL: %s" % url, e)

    def start(self):
        """Start the connection to RabbitMQ

        This method will connect to RabbitMQ, and setup the exchange and queue
        automatically.
        """
        self._connect()
        self._init_exchange()
        self._init_queue()
        self._bind_queue()

    def stop(self):
        try:
            self._connection.close()
        except AttributeError as e:
            pass
        except pika.exceptions.ConnectionClosed as e:
            pass
        
    
    def send(self, json):
        """Send JSON message

        This method will publish a JSON string to the RabbitMQ server
        """
        try:
            retval = self._channel.basic_publish(
                exchange=self.exchange_config['name'],
                routing_key=self.queue_config['name'],
                body=json,
                mandatory=True,
                properties=self._msg_properties
            )

            if retval == False:
                raise exceptions.MessageNotSentException("Message not sent, enable pika logging for more information")
        except Exception as e:
            raise exceptions.ConnectionException("Connection error", e)

    def connected(self):
        if self._connection:
            if self._connection.is_closed == True:
                return False
            elif self._connection.is_open == False:
                return False
            else:
                return True
        else:
            return False

    def _connect(self):
        try:
            self._connection = pika.BlockingConnection(self._params)
            self._channel = self._connection.channel()
        except Exception as e:
            raise exceptions.ConnectionException("Trouble connecting to the RabbitMQ server", e)


    def _init_exchange(self):
        try:
            self._channel.exchange_declare(
                exchange=self.exchange_config['name'],
                type=self.exchange_config['type'],
                durable=self.exchange_config['durable'],
                auto_delete=self.exchange_config['autodelete']
            )
        except Exception as e:
            raise exceptions.ExchangeException("Failed to declare exchange", e)
       
    def _init_queue(self):
        try:
            self._channel.queue_declare(
                queue=self.queue_config['name'],
                durable=self.queue_config['durable'],
                exclusive=self.queue_config['exclusive'],
                auto_delete=self.queue_config['autodelete'],
                arguments={
                    'x-message-ttl': self.queue_config['ttl']
                }
            )
        except Exception as e:
            raise exceptions.QueueException("Failed to declare queue", e)



    def _bind_queue(self):
        try:
            self._channel.queue_bind(
                queue=self.queue_config['name'],
                exchange=self.exchange_config['name'],
                routing_key=self.queue_config['name']
            )
        except Exception as e:
            raise exceptions.QueueException("Failed to bind to queue", e)       

