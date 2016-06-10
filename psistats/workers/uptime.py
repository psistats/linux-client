from psistats.workerThread import WorkerThread
from psistats import uptime
import os

class UptimeWorker(WorkerThread):

    def work(self):
        return {'uptime': uptime.uptime() }
