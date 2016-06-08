from psistats.workerThread import WorkerThread
from psistats import system

class CpuWorker(WorkerThread):
    
    def work(self):
        return {'cpu': system.get_cpu_usage(True) }
