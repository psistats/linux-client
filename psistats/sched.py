import time
from threading import Thread
import logging
import json

class Interval(Thread):
    def __init__(self, interval, worker):
        Thread.__init__(self)
        self._interval = interval
        self._worker = worker
        self._running = False
        self._appConfig = None

    def stop(self):
        self._running = False
        self.join()

    def start(self, appConfig):
        self._appConfig = appConfig
        self._running = True
        super(Interval, self).start()

    def run(self):
        self._running = True
        

class QueueInterval(Interval):
    def __init__(self, interval, worker, queue):
        Interval.__init__(self, interval, worker)
        self._queue = queue
        self._logger = logging.getLogger('psistats')
        self._counter = self._interval

    def send_packet(self, packet):
        packetStr = json.dumps(packet)
        self._logger.debug('Sending packet: %s', packetStr)
        self._queue.send(packetStr)

    def run(self):
        while self._running == True:
            if self._counter == self._interval:
                self.send_packet(self._worker(self._appConfig))
                self._counter = 0
            else:
                time.sleep(1)
                self._counter += 1
