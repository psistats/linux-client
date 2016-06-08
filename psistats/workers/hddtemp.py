from psistats.workerThread import WorkerThread
from psistats import hdd

class HddTempWorker(WorkerThread):
    
    def work(self):
        host = self._config['hddtemp']['hostname']
        port = self._config['hddtemp']['port']
        return {'hddtemp': hdd.get_hdd_temps(host, port)}
