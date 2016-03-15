'''
Created on Jun 21, 2014

@author: v0idnull
'''
from psistats import stats
from psistats import queue
from sched import QueueInterval
from psistats.sensors import sensors as libsensors
import time
import logging
import logging.config as loggingconfig
import sys
import simplejson as json
from psistats.exceptions import MessageNotSentException, ConnectionException, QueueException, ExchangeException
import psutil


def ipaddr(appConfig):
    return {
        'ipaddr': stats.ipaddr()
    }

def mem(appConfig):
    return {
        'mem': stats.mem()
    }

def hddspace(appConfig):
    return {
        'hddspace': None
    }

def hddtemps(appConfig):
    return {
        'hddtemps': stats.hddtemps(appConfig['hddtemp']['hostname'], appConfig['hddtemp']['port'])
    }

def cpu(appConfig):
    return {
        'cpu': stats.cpu(per_cpu=True)
    }
     

def sensors(appConfig):
    devices = stats.sensors(appConfig['sensors']['devices'])

    return {
        'sensors': devices
    }

def hddspace(appConfig):
    devices = stats.hdds()

    deviceSpaces = {}

    for device in devices:
        deviceSpaces[device] = stats.hddspace(device)

    return {
        'hddspace': deviceSpaces
    }

class App(object):

    reporters = [
        ('ipaddr', ipaddr),
        ('mem', mem),
        ('sensors', sensors),
        ('cpu', cpu),
        ('hddspace', hddspace),
        ('hddtemp', hddtemps)
    ]

    def __init__(self, config):
        self.config = config
        self.logger = None
        self._events = None

        self.pidfile_path = config['app']['pidfile']
        self.pidfile_timeout = config['app']['pidfile_timeout']
        
        self._running = False

        self._init_logger()

        self._connection = None
        self._channel = None

        self._reporterThreads = {}

    def _init_logger(self):
        logger_config = self.config['logging']

        loggingconfig.dictConfig(logger_config)
        logger = logging.getLogger("psistats")
        self.logger = logger

    def init_queue(self):
        self.queue = queue.Queue(self.config['server']['url'], self.config['queue'], self.config['exchange'])
        return self.queue

    def _send_packet(self, packet):
        packet_json = json.dumps(packet)
        self.logger.debug('Sending packet: %s' % packet_json)
        self.queue.send(packet_json)

    def prepare_packet(self, keys):
        packet = {}

        for key in keys:
            statfunc = getattr(stats, key)
            packet[key] = statfunc() if self.config[key]['enabled'] == True else None

        return packet

    def _loop(self):
        # used as a counter to determine interval to
        # send uptime and ip address updates

        while self._running == True:
            time.sleep(1)


    def run(self):
        self.logger.info("Starting")

        hostname = stats.hostname()

        self.config['queue']['name'] = self.config['queue']['prefix'] + '.' + hostname
        
        try:
            queue = self.init_queue()
            queue.start()

            for reporterName, reporterCb in self.reporters:
                if self.config[reporterName]['enabled'] == 0:
                    self.logger.debug('Reporter %s is disabled' % reporterName)
                else:
                    self.logger.debug('Revving up %s', reporterName)
                    self._reporterThreads[reporterName] = QueueInterval(self.config[reporterName]['interval'], reporterCb, queue)
                    self._reporterThreads[reporterName].start(self.config)

            self._running = True
            self._loop()
        except KeyboardInterrupt:
            self.logger.warn("Received keyboard interrupt")
        except:
            self.logger.critical("Unhandled exception")
            self.logger.exception(sys.exc_info()[1])
        finally:
            self._running = False
            self.logger.warn("Shutting down")
            for reporter in self._reporterThreads.iterkeys():
                self.logger.debug('Stopping thread: %s', reporter)
                reporterThread = self._reporterThreads[reporter]
                reporterThread.stop()
            queue.stop()

