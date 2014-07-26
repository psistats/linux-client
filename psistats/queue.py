'''
Created on Jun 21, 2014

@author: v0idnull
'''
import pika


def get_connection(config):
    credentials = pika.PlainCredentials(config['user'], config['pass'])

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        config['host'],
        config['port'],
        config['path'],
        credentials
    ))
    return connection


def ping(config):
    connection = get_connection(config)
    channel = connection.channel()
    connection.close()

def send_json(json, channel, exchange_name, queue_name):
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=queue_name,
        body=json,
        properties=pika.spec.BasicProperties(
            content_type="application/json",
            content_encoding="utf-8"
        )
    )


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
