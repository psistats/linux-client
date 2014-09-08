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


class Main(object):

    def __init__(self, config):
        self.config = config
        self.logger = None

        self.stdin_path = config['app']['stdin_path']
        self.stdout_path = config['app']['stdout_path']
        self.stderr_path = config['app']['stderr_path']
        self.pidfile_path = config['app']['pidfile']
        self.pidfile_timeout = config['app']['pidfile_timeout']

    def get_logger(self):
        if self.logger == None:

            logger_config = self.config['logging']

            loggingconfig.dictConfig(logger_config)
            logger = logging.getLogger("psistats")
            self.logger = logger
        return self.logger

    def run(self):
        logger = self.get_logger()
        logger.info("Starting")

        hostname = stats.hostname()

        config = self.config

        config['queue']['name'] = config['queue']['prefix'] + '.' + hostname

        connected = False
        connection = None
        channel = None

        # used as a counter to determine interval to
        # send uptime and ip address updates
        meta_refresh_counter = config['app']['meta_timer']

        sleep = config['app']['timer']

        try:

            while True:

                try:

                    if connected == False:
                        logger.info("Creating connection")
                        logger.debug("get connection")
                        connection = get_connection(self.config['server'])

                        logger.debug("get channel")
                        channel = connection.channel()

                        logger.debug("setup queue")
                        setup_queue(channel, self.config['exchange'], self.config['queue'])

                        connected = True

                    packet = {
                        'hostname': hostname,
                        'cpu': stats.cpu(),
                        'mem': stats.mem()
                    }

                    if meta_refresh_counter == config['app']['meta_timer']:
                        packet['ipaddr'] = stats.ip4_addresses()
                        packet['uptime'] = stats.uptime()
                        meta_refresh_counter = 1

                    if config['cpu_temp']['enabled']:
                        packet['cpu_temp'] = stats.cpu_temp()

                    packet_json = json.dumps(packet)
                    logger.debug('Sending packet: %s' % packet_json)
                    send_json(packet_json, channel, config['exchange']['name'], config['queue']['name'])

                    meta_refresh_counter += 1

                    time.sleep(sleep)

                except (AMQPConnectionError, ChannelClosed) as e:
                    logger.critical("Connection error with RabbitMQ!")
                    logger.exception(e)
                    logger.debug('Retrying in %i seconds' % config['app']['retry_timer'])
                    connected = False
                    if connection != None and connection.is_closed == False:
                        try:
                            connection.close()
                        except ConnectionClosed:
                            pass
                    connection = None

                    time.sleep(config['app']['retry_timer'])
                except AttributeError as e:
                    logger.exception(sys.exc_info()[1])
                    logger.error("This could be caused by a problem with the RabbitMQ server!! We are going to restart the connection to be safe!!")
                    connection = None
                    channel = None
                    connected = False
                except MessageNotSent as e:
                    logger.exception(sys.exc_info()[1])
                    logger.error("MessageNotSent exception - this could be caused by RabbitMQ shutting down, or the queue being deleted. Resetting connection to be sure.")
                    connection = None
                    channel = None
                    connected = False

        except KeyboardInterrupt:
            logger.warn("Received keyboard interrupt")
        except:
            logger.critical("Unhandled exception")
            logger.exception(sys.exc_info()[1])
        finally:
            logger.warn("Shutting down")
            if (connected == True):
                connection.close()
