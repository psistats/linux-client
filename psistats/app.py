'''
Created on Jun 21, 2014

@author: v0idnull
'''
import time
import logging
import logging.config as loggingconfig
import sys
import simplejson as json
import psutil

from psistats.exceptions import MessageNotSentException, ConnectionException, QueueException, ExchangeException
from psistats import queue
from psistats import net
from psistats import system
from psistats import libsensors
from psistats import hdd
from psistats.libsensors import Sensors
from psistats.workerThread import WorkerThread

def ipaddr(appConfig):
    return {
        'ipaddr': net.get_ipaddrs()
    }

def mem(appConfig):
    return {
        'mem': system.get_mem_usage()
    }

def hddspace(appConfig):
    return {
        'hddspace': hdd.get_hdd_space()
    }

def hddtemps(appConfig):
    return {
        'hddtemps': hdd.get_hdd_temps(appConfig['hddtemp']['hostname'], appConfig['hddtemp']['port'])
    }

def cpu(appConfig):
    return {
        'cpu': system.get_cpu_usage(True)
    }
     



def sensors(appConfig):

    if hasattr(sensors, 'libsensor') == False:

        s = Sensors()
        s.init()
        for chipName in appConfig['sensors']['devices']:
            print "chipName: %s" % chipName
            s.add_chip(chipName)

        setattr(sensors, 'libsensor', s)


    devices = {}

    for chipName in appConfig['sensors']['devices'].iterkeys():
        chip = appConfig['sensors']['devices'][chipName]

        if chipName not in devices:
            devices[chipName] = {}

        for featureName in chip.iterkeys():
            v, unit = sensors.libsensor.get_value(chipName, featureName)
            devices[chipName][featureName] = {
                'label': chip[featureName],
                'value': v,
                'unit': unit
            }
    return {
        'sensors': devices
    }


def hddspace(appConfig):

    devices = hdd.get_hdds()

    deviceSpaces = {}

    for device in devices:
        deviceSpaces[device] = hdd.get_hdd_space(device)

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

    def prepare_packet(self, keys):
        packet = {}

        for key in keys:
            statfunc = getattr(stats, key)
            packet[key] = statfunc() if self.config[key]['enabled'] == True else None

        return packet

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
            for reporterName, reporterCb in self.reporters:
                self._reporterThreads[reporterName] = WorkerThread(self.config[reporterName]['interval'], reporterCb, self.config)

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

