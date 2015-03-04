import pika
import unittest
import mock
from psistats import queue
from psistats import exceptions
import logging
import sys
import socket
class QueueConnectionTest(unittest.TestCase):

    class FakeChannel():
        def exchange_declare(self, callback=None, exchange=None,
            exchange_type='direct', passive=False, durable=False,
            auto_delete=False, internal=False, nowait=False,
            arguments=None, type=None):
            pass

        def queue_bind(self, callback, queue, exchange, routing_key=None,
            nowait=False, arguments=None):
            pass

        def queue_declare(self, callback, queue='', passive=False, durable=False,
            exclusive=False, auto_delete=False, nowait=False,
            arguments=None):
            pass

        

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


    def test_badQueueDeclare(self):
        mockchannel = self.FakeChannel()

        patcher = mock.patch.object(mockchannel, 'queue_declare', side_effect=self._raiseAMQPException)
        patcher.start()

        self.assertRaises(
            exceptions.QueueException, 
            queue.setup_queue, 
            mockchannel, 
            {"name": "test", "type": "test", "durable": "test", "autodelete": "test"},
            {"name": "test", "type": "test", "durable": "test", "autodelete": "test"}
        )

        patcher.stop() 

    def test_badQueueBind(self):
        mockchannel = self.FakeChannel()

        patcher = mock.patch.object(mockchannel, 'queue_bind', side_effect=self._raiseAMQPException)
        patcher.start()

        self.assertRaises(
            exceptions.QueueException, 
            queue.setup_queue, 
            mockchannel, 
            {"name": "test", "type": "test", "durable": "test", "autodelete": "test"},
            {"name": "test", "type": "test", "durable": "test", "autodelete": "test"}
        )


        patcher.stop()

    def test_badExchangeDeclare(self):
        mockchannel = self.FakeChannel()

        patcher = mock.patch.object(mockchannel, 'exchange_declare', side_effect=self._raiseAMQPException)
        patcher.start()

        self.assertRaises(
            exceptions.ExchangeException, 
            queue.setup_queue, 
            mockchannel, 
            {"name": "test", "type": "test", "durable": "test", "autodelete": "test"},
            {"name": "test", "type": "test", "durable": "test", "autodelete": "test"}
        )

        patcher.stop() 
