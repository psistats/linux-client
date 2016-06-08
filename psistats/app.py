'''
Created on Jun 21, 2014

@author: v0idnull
'''
import time
import logging
import logging.config as loggingconfig
import sys
import simplejson as json

from psistats.exceptions import MessageNotSentException, ConnectionException, QueueException, ExchangeException
from psistats import queue
from psistats import net
from psistats import system
from psistats import libsensors
from psistats import hdd
from psistats.libsensors import Sensors
from psistats.workerThread import WorkerThread
from psistats.workers.cpu import CpuWorker
from psistats.workers.mem import MemWorker
from psistats.workers.ipaddr import IPAddrWorker
from psistats.workers.hddspace import HddSpaceWorker
from psistats.workers.hddtemp import HddTempWorker
from psistats.workers.sensors import SensorsWorker

    
class App(object):

    reporters = [
        ('ipaddr', IPAddrWorker),
        ('mem', MemWorker),
        ('sensors', SensorsWorker),
        ('cpu', CpuWorker),
        ('hddspace', HddSpaceWorker),
        ('hddtemp', HddTempWorker)
    ]

    def __init__(self, config):
        self.config = config
        self.logger = None
        self._events = None

        self.pidfile_path = config['app']['pidfile']
        self.pidfile_timeout = config['app']['pidfile_timeout']
        self.stdin_path = config['app']['stdin_path']
        self.stdout_path = config['app']['stdout_path']
        self.stderr_path = config['app']['stderr_path']
        
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

    def _loop(self):
        while self._running == True:
            for reporterName, reporterThread in self._reporterThreads.iteritems():
                if reporterThread.running() == False:
                    self.logger.debug('Thread %s is not running. Restarting it' % reporterName)
                    reporterThread.start()

            time.sleep(10)

    def startWorkerThread(self, thread):
        try:
            thread.start()
        except ConnectionException as e:
            self.logger.error('Error starting thread')
            self.logger.exception(e)

    def run(self):
        self.logger.info("Starting")

        hostname = net.get_hostname()

        self.config['queue']['name'] = self.config['queue']['prefix'] + '.' + hostname
        
        try:
            for reporterName, worker in self.reporters:
                self._reporterThreads[reporterName] = worker(self.config[reporterName]['interval'], self.config)

                try:
                    self._reporterThreads[reporterName].start()
                except ConnectionException as e:
                    self.logger.error('Error starting thead: %s' % reporterName)
                    self.logger.exception(e)

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

