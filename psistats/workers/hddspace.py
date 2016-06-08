from psistats.workerThread import WorkerThread
from psistats import hdd

class HddSpaceWorker(WorkerThread):
    
    def work(self):
        return {'hddspace': hdd.get_hdd_space()} 
