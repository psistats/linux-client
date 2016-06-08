from psistats.workerThread import WorkerThread
from psistats import net

class IPAddrWorker(WorkerThread):
    
    def work(self):
        return {'ipaddr': net.get_ipaddrs() }
