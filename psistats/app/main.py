'''
Created on Jun 21, 2014

@author: v0idnull
'''
from psistats import stats
import time
import logging
import logging.config as loggingconfig
import sys
import simplejson as json
from psistats.queue import get_connection, setup_queue, send_json, ping
from pika.exceptions import AMQPConnectionError, ConnectionClosed, ChannelClosed
from psistats.exceptions import MessageNotSent
import socket
import warnings

class Main(object):

    def __init__(self, config):
        self.config = config
        self.logger = None

        self.stdin_path = config['app']['stdin_path']
        self.stdout_path = config['app']['stdout_path']
        self.stderr_path = config['app']['stderr_path']
        self.pidfile_path = config['app']['pidfile']
        self.pidfile_timeout = config['app']['pidfile_timeout']

    def _init_logger(self):
        if self.logger == None:

            logger_config = self.config['logging']

            loggingconfig.dictConfig(logger_config)
            logger = logging.getLogger("psistats")
            self.logger = logger
        return self.logger
    
    def _init_connection(self):
        self.logger.info("Creating connection")
        self.logger.debug("get connection")
        self.connection = get_connection(self.config['server'])

        self.logger.debug("get channel")
        self.channel = self.connection.channel()

        self.logger.debug("setup queue")
        setup_queue(self.channel, self.config['exchange'], self.config['queue'])

        self.connected = True


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
        send_json(packet_json, self.channel, self.config['exchange']['name'], self.config['queue']['name'])

    def _secondary_task(self):
        packet = {
            'hostname': stats.hostname(),
            'ipaddr': stats.ip4_addresses(),
            'uptime': stats.uptime()
        }

        packet_json = json.dumps(packet)
        self.logger.debug('Sending packet: %s' % packet_json)
        send_json(packet_json, self.channel, self.config['exchange']['name'], self.config['queue']['name'])


    def _loop(self):
        # used as a counter to determine interval to
        # send uptime and ip address updates
        secondary_timer = self.config['app']['secondary_timer']
        primary_timer = self.config['app']['primary_timer']

        while True:
            try:
                if self.connected == False:
                    self._init_connection()
                self._primary_task()
                if secondary_timer == self.config['app']['secondary_timer']:
                    self._secondary_task()
                    secondary_timer = 1
                else:
                    secondary_timer = secondary_timer + 1
                time.sleep(primary_timer)
            except (AMQPConnectionError, ChannelClosed, socket.error) as e:
                self.logger.critical("Connection error with RabbitMQ!")
                self.logger.exception(e)
                self.logger.debug('Retrying in %i seconds' % self.config['app']['retry_timer'])
                self.connection = None
                self.channel = None
                self.connected = False
                time.sleep(self.config['app']['retry_timer'])
            except AttributeError as e:
                self.logger.exception(sys.exc_info()[1])
                self.logger.error("This could be caused by a problem with the RabbitMQ server!! We are going to restart the connection to be safe!!")
                self.connection = None
                self.channel = None
                self.connected = False
            except MessageNotSent as e:
                self.logger.exception(e)
                self.logger.error("MessageNotSent exception - this could be caused by RabbitMQ shutting down, or the queue being deleted. Resetting connection to be sure.")
                self.connection = None
                self.channel = None
                self.connected = False
            except UserWarning as e:
                self.logger.exception(e)
                self.logger.error('UserWarning exception - this could be caused by a connection error with RabbitMQ. Resetting the connection to be sure.')
                self.connection = None
                self.channel = None
                self.connected = False



    def run(self):
        logger = self._init_logger()
        logger.info("Starting")

        warnings.filterwarnings('error', '.*Write buffer exceeded warning threshold.*')

        hostname = stats.hostname()

        self.config['queue']['name'] = self.config['queue']['prefix'] + '.' + hostname

        self.connected = False
        self.connection = None
        self.channel = None

        try:
            self._loop()
        except KeyboardInterrupt:
            logger.warn("Received keyboard interrupt")
        except:
            logger.critical("Unhandled exception")
            logger.exception(sys.exc_info()[1])
        finally:
            logger.warn("Shutting down")
            if self.connected == True:
                self.connection.close()
