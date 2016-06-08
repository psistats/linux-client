from psistats.workerThread import WorkerThread
from psistats import system

class MemWorker(WorkerThread):
    
    def work(self):
        return {'mem': system.get_mem_usage() }
