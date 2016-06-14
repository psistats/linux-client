from psistats.workerThread import WorkerThread
from psistats import system

class OSWorker(WorkerThread):
    def work(self):
        return {'os': system.get_distro()}

