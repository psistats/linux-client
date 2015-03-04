import pika
import unittest
import mock
from psistats import queue
from psistats import exceptions
import logging
import sys
import socket
class QueueConnectionTest(unittest.TestCase):

    def _raiseAMQPException(self):
        raise Exception("failed")

    @mock.patch('psistats.queue.pika.BlockingConnection')
    def test_badUrls(self, mock_BlockingConnection):


        self.assertRaises(exceptions.QueueConfigException, queue.get_connection, ('noscheme'))
        self.assertRaises(exceptions.QueueConfigException, queue.get_connection, (1))

        self.assertRaises(exceptions.QueueConfigException, queue.get_connection, ('amqp://hostname:abcd'))


    @mock.patch('psistats.queue.pika.BlockingConnection', side_effect=_raiseAMQPException)
    def test_badConnection(self, mock_BlockingConnection):
        self.assertRaises(exceptions.QueueConnectionException, queue.get_connection, ('amqp://guest:guest@1.1.1.1:5672'))


    
