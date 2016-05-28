import time
from threading import Thread
import logging
import json
from queue import Queue
from exceptions import ConnectionException

class WorkerThread(Thread):
    def __init__(self, interval, worker, config):
        self._worker = worker
        self._config = config
        self._running = False
        self._interval = interval
        self._counter = interval
        self._logger = logging.getLogger('psistats')
        super(WorkerThread, self).__init__()

    def start(self):
        self._queue = Queue(self._config['server']['url'], self._config['queue'], self._config['exchange'])
        self._queue.start()
        super(WorkerThread, self).start()

    def stop(self):
        self._running = False
        self.join()
        self._queue.stop()
       
    def send_packet(self, obj):
        packet = json.dumps(obj)
        self._logger.debug(packet)
        self._queue.send(json.dumps(obj))

    def loop(self):
        if self._counter == self._interval:
            self.send_packet(self._worker(self._config))
            self._counter = 0
        else:
            time.sleep(1)
            self._counter += 1       
       

    def run(self):
        self._running = True

        while self._running == True:
            try:
                self.loop()
            except ConnectionException as e:
                self._logger.error(e.message)
                self._running = False

    def running(self):
        return self._running

