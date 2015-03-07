import pika
import unittest
import mock
from psistats import queue
from psistats import exceptions
from psistats.queue import Queue
import logging
import sys
import socket

class QueueTest(unittest.TestCase):

    QUEUE_CONFIG = {
        'name': 'psistats',
        'durable': False,
        'exclusive': False,
        'autodelete': False,
        'ttl': 10000
    }

    EXCHANGE_CONFIG = {
        'name': 'psistats',
        'type': 'topic',
        'autodelete': False,
        'durable': False
    }

    def test_badUrls(self):
        self.assertRaises(exceptions.ConfigException, Queue, 'blah', self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)
        self.assertRaises(exceptions.ConfigException, Queue, 1, self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)
        self.assertRaises(exceptions.ConfigException, Queue, 'amqp://hostname:abcd', self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)

    @mock.patch('psistats.queue.pika.BlockingConnection', side_effect=Exception)
    def test_badConnection(self, mock_BlockingConnection):
        q = Queue('amqp://1.1.1.1', self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)
        self.assertRaises(exceptions.ConnectionException, q.start)

    @mock.patch('psistats.queue.pika.BlockingConnection')
    def test_badChannel(self, mock_BlockingConnection):

        mock_config = {
            'return_value.channel.side_effect': Exception
        }
        mock_BlockingConnection.configure_mock(**mock_config)
 
        q = Queue('amqp://1.1.1.1', self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)
        self.assertRaises(exceptions.ConnectionException, q.start)

    @mock.patch('psistats.queue.pika.BlockingConnection')
    def test_badExchange(self, mock_BlockingConnection):

        mock_config = {
            'return_value.channel.return_value.exchange_declare.side_effect': Exception
        }
        mock_BlockingConnection.configure_mock(**mock_config)

        q = Queue('amqp://1.1.1.1', self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)        
        self.assertRaises(exceptions.ExchangeException, q.start)

    @mock.patch('psistats.queue.pika.BlockingConnection')
    def test_badQueue(self, mock_BlockingConnection):
        mock_config = {
            'return_value.channel.return_value.queue_declare.side_effect': Exception
        }
        mock_BlockingConnection.configure_mock(**mock_config)
        
        q = Queue('amqp://1.1.1.1', self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)
        self.assertRaises(exceptions.QueueException, q.start)

        mock_config = {
            'return_value.channel.return_value.queue_bind.side_effect': Exception,
            'return_value.channel.return_value.queue_declare.side_effect': None
        }
        mock_BlockingConnection.configure_mock(**mock_config)
        q = Queue('amqp://1.1.1.1', self.QUEUE_CONFIG, self.EXCHANGE_CONFIG)
        self.assertRaises(exceptions.QueueException, q.start)

