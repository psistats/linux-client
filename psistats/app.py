'''
Created on Jun 21, 2014

@author: v0idnull
'''
from psistats import stats
from psistats import queue
import time
import logging
import logging.config as loggingconfig
import sys
import simplejson as json
from psistats.exceptions import MessageNotSentException, ConnectionException, ConfigException, QueueException, ExchangeException
import socket
import warnings

class App():

    def __init__(self, config):
        self.config = config
        self.logger = None

        self.stdin_path = config['app']['stdin_path']
        self.stdout_path = config['app']['stdout_path']
        self.stderr_path = config['app']['stderr_path']
        self.pidfile_path = config['app']['pidfile']
        self.pidfile_timeout = config['app']['pidfile_timeout']
        self.queue = queue.Queue(config['server']['url'], config['queue'], config['exchange'])

        self._init_logger()

        self._connection = None
        self._channel = None

    def _init_logger(self):
        logger_config = self.config['logging']

        loggingconfig.dictConfig(logger_config)
        logger = logging.getLogger("psistats.app")
        self.logger = logger

    def _primary_task(self):
        packet = {
            'hostname': stats.hostname(),
            'cpu': stats.cpu(),
            'mem': stats.mem()
        }
        if self.config['cpu_temp']['enabled']:
            packet['cpu_temp'] = stats.cpu_temp()        

        packet_json = json.dumps(packet)
        self.logger.debug('Sending packet: %s' % packet_json)
        self.queue.send(packet_json)

    def _secondary_task(self):
        packet = {
            'hostname': stats.hostname(),
            'ipaddr': stats.ip4_addresses(),
            'uptime': stats.uptime()
        }

        packet_json = json.dumps(packet)
        self.logger.debug('Sending packet: %s' % packet_json)
        self.queue.send(packet_json)


    def _loop(self):
        # used as a counter to determine interval to
        # send uptime and ip address updates
        secondary_timer = self.config['app']['secondary_timer']
        primary_timer = self.config['app']['primary_timer']

        while True:
            try:
                if self.queue.connected() == False:
                    self.queue.start()

                self._primary_task()

                if secondary_timer == self.config['app']['secondary_timer']:
                    self._secondary_task()
                    secondary_timer = 1
                else:
                    secondary_timer = secondary_timer + 1

                time.sleep(primary_timer)

            except ConnectionException as e:
                self.logger.warn("Connection error")
                self.logger.exception(e)
                self.queue.stop()
                time.sleep(self.config['app']['retry_timer'])
            except QueueException as e:
                self.logger.warn("Queue error")
                self.logger.exception(e)
                time.sleep(self.config['app']['retry_timer'])
            except MessageNotSentException as e:
                self.logger.warn("Unable to send message")
                self.logger.exception(e)
            except ExchangeException as e:
                self.logger.exception(e)
                self.logger.error('UserWarning exception - this could be caused by a connection error with RabbitMQ. Resetting the connection to be sure.')
                


    def run(self):
        self.logger.info("Starting")

        warnings.filterwarnings('error', '.*Write buffer exceeded warning threshold.*')

        hostname = stats.hostname()

        self.config['queue']['name'] = self.config['queue']['prefix'] + '.' + hostname

        try:
            self._loop()
        except KeyboardInterrupt:
            self.logger.warn("Received keyboard interrupt")
        except:
            self.logger.critical("Unhandled exception")
            self.logger.exception(sys.exc_info()[1])
        finally:
            self.logger.warn("Shutting down")
