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
from psistats.workers.uptime import UptimeWorker
from psistats.workers.os import OSWorker
    
class App(object):
    """
    Application Class

    This is the main loop
    """

    reporters = [
        ('ipaddr', IPAddrWorker),
        ('mem', MemWorker),
        ('sensors', SensorsWorker),
        ('cpu', CpuWorker),
        ('hddspace', HddSpaceWorker),
        ('hddtemp', HddTempWorker),
        ('uptime', UptimeWorker),
        ('os', OSWorker)
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

        self._connection = None
        self._channel = None

        self._reporterThreads = {}

    def _init_logger(self):
        logger_config = self.config['logging']

        loggingconfig.dictConfig(logger_config)
        logger = logging.getLogger("psistats")
        self.logger = logger

 
    def _init_workers(self):
        for reporterName, worker in self.reporters:

            if reporterName not in self.config:
                self.logger.warn('Reporter %s not in configuration' % reporterName)
                continue

            if 'enabled' not in self.config[reporterName] or self.config[reporterName]['enabled'] == False:
                self.logger.warn('Reporter %s is disabled' % reporterName)
                continue


            workerThread = worker(self.config[reporterName]['interval'], self.config)
            self._reporterThreads[reporterName] = workerThread
       

    def work(self):
        for reporterName, reporterThread in self._reporterThreads.iteritems():
            if reporterThread.running() == False:
                self.logger.debug('Starting thread %s' % reporterName)
                self.startWorkerThread(reporterThread)


    def isRunning(self):
        return self._running


    def startWorkerThread(self, thread):
        """
        Starts a worker thread.

        Each worker thread is expected to have its own connection to
        the message queue. If a ConnectionException is raised, it is
        logged and ignored.
        """
        try:
            thread.start()
        except ConnectionException as e:
            self.logger.error('Error starting thread')
            self.logger.exception(e)


    def stop(self):
        self._running = False

        for reporterName in self._reporterThreads:
            self.logger.debug('Stopping thread: %s', reporterName)
            self._reporterThreads[reporterName].stop()


    def start(self):
        self._init_logger()
        self.logger.info("Starting")

        hostname = net.get_hostname()
        self.config['queue']['name'] = self.config['queue']['prefix'] + '.' + hostname

        self._init_workers()

        self.run()


    def run(self):
        self._running = True
        try:
            while self.isRunning():
                self.work()
                time.sleep(10)
            self.stop()
        except KeyboardInterrupt:
            self.logger.warn("Received keyboard interrupt")
            self.stop()
        except:
            self.logger.critical("Unhandled exception")
            self.logger.exception(sys.exc_info()[1])
            self.stop()

