from psistats.workerThread import WorkerThread
from psistats import hdd

class HddSpaceWorker(WorkerThread):
    
    def start(self):
        self._hdds = hdd.get_hdds()
        super(HddSpaceWorker, self).start()

    def work(self):
        obj = {'hddspace': []}
        for drive in self._hdds:
            drvobj = {}
            drvobj[drive] = hdd.get_hdd_space(drive)
            obj['hddspace'].append(drvobj)

        return obj
