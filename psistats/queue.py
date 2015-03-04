'''
Created on Jun 21, 2014

@author: v0idnull
'''
import pika
from psistats import exceptions
from urlparse import urlparse

def get_connection(url):

    try:
        params = pika.URLParameters(url)
    except Exception as e:
        raise exceptions.QueueConfigException("Invalid URL: %s" % url, e)

    print params    
    try:
        connection = pika.BlockingConnection(params)
    except Exception as e:
        raise exceptions.QueueConnectionException("Trouble connecting to the RabbitMQ server", e)
    return connection


def ping(config):
    connection = get_connection(config)
    channel = connection.channel()
    connection.close()

def send_json(json, channel, exchange_name, queue_name):
    retval = channel.basic_publish(
        exchange=exchange_name,
        routing_key=queue_name,
        mandatory=True,
        body=json,
        properties=pika.spec.BasicProperties(
            content_type="application/json",
            content_encoding="utf-8"
        )
    )

    if retval == False:
        raise exceptions.MessageNotSentException("Message not sent, enable pika logging for more information")


def setup_queue(channel, exchange_config, queue_config):

    channel.exchange_declare(
        exchange=exchange_config['name'],
        type=exchange_config['type'],
        durable=exchange_config['durable'],
        auto_delete=exchange_config['autodelete']
    )

    channel.queue_declare(
        queue=queue_config['name'],
        durable=queue_config['durable'],
        exclusive=queue_config['exclusive'],
        auto_delete=queue_config['autodelete'],
        arguments={
            'x-message-ttl': queue_config['ttl']
        }
    )

    channel.queue_bind(
        queue=queue_config['name'],
        exchange=exchange_config['name'],
        routing_key=queue_config['name']
    )
