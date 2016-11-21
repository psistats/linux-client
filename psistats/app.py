import time
import logging
import logging.config as loggingconfig
import sys
import os

from psistats import net
from psistats.exceptions import ConnectionException
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

        self.pidfile_path = config['app']['pidfile']
        self.pidfile_timeout = config['app']['pidfile_timeout']
        self.stdout_path = config['app']['stdout_path']
        self.stderr_path = config['app']['stderr_path']
        
        self._running = False
        self._reporters_initialized = False
        self._reporterThreads = {}

        self.init_logger()


    def init_logger(self):
        """
        Initialize the logger
        """
        logger_config = self.config['logging']

        loggingconfig.dictConfig(logger_config)
        logger = logging.getLogger("psistats")
        self.logger = logger

 
    def init_reporters(self):
        """
        Initialize the configured reporters
        """
        for reporterName, worker in self.reporters:

            if reporterName not in self.config:
                self.logger.warn('Reporter %s not in configuration' % reporterName)
                continue

            if 'enabled' not in self.config[reporterName] or self.config[reporterName]['enabled'] == False:
                self.logger.warn('Reporter %s is disabled' % reporterName)
                continue


            workerThread = worker(self.config[reporterName]['interval'], self.config)
            self._reporterThreads[reporterName] = workerThread
        self._reporters_initialized = True

    
    def reporter(self, name):
        """
        Get an initialized reporter thread
        """
        return self._reporterThreads[name]
       

    def work(self):
        """
        Do an iteration of work
        """
        if self._reporters_initialized == False:
            self.init_reporters()

        for reporterName in self._reporterThreads:
            reporter = self._reporterThreads[reporterName]
            if reporter.running() == False:
                self.logger.debug('Starting thread %s' % reporterName)
                self.start_reporter_thread(reporter)


    def is_running(self):
        """
        Checks if application is running or not
        """
        return self._running


    def start_reporter_thread(self, thread):
        """
        Starts a reporter thread.

        Each reporter thread is expected to have its own connection to
        the message queue. If a ConnectionException is raised, it is
        logged and ignored.
        """
        try:
            thread.start()
        except ConnectionException as e:
            self.logger.error('Error starting thread')
            self.logger.exception(e)


    def stop(self):
        """
        Stop running the application and all reporter threads
        """
        self._running = False

        for reporterName in self._reporterThreads:
            self.logger.debug('Stopping thread: %s', reporterName)
            self._reporterThreads[reporterName].stop()

        os.remove(self.config['app']['pidfile'])


    def start(self):
        """
        Start running the application all reporter threads
        """
        self.logger.info("Starting")

        pid = os.getpid()

        with open(self.config['app']['pidfile'], 'w') as f:
            f.write(str(pid))

        hostname = net.get_hostname()
        self.config['queue']['name'] = self.config['queue']['prefix'] + '.' + hostname

        self.run()


    def reporter_running(self, reporterName):
        """
        Check if a reporter of a specific name is running
        """
        if reporterName not in self._reporterThreads:
            return False

        return self._reporterThreads[reporterName].running()


    def run(self):
        """
        Run the application loop
        """
        self._running = True
        try:
            while self.is_running() == True:
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

