from psistats.workerThread import WorkerThread
from psistats.libsensors import Sensors

class SensorsWorker(WorkerThread):

    def __init__(self, interval, config):
        super(WorkerThread, self).__init__(interval, config)
        self._sensors = None

    def start(self):
        if self._sensors == None:
            self._sensors = Sensors()
            s.init()
            for chipName in self._config['sensors']['devices']:
                s.add_chip(chipName)
        return super(WorkerThread, self).start()

    def work(self):
        devices = {}
        for chipName in self._config['sensors']['devices'].iterkeys():
            chip = self._config['sensors']['devices'][chipName]

            if chipName not in devices:
                devices[chipName] = {}

            for featureName in chip.iterkeys():
                v, unit = self._sensors.get_value(chipName, featureName)
                devices[chipName][featureName] = {
                    'label': chip[featureName],
                    'value': v,
                    'unit': unit
                }
        return {
            'sensors': devices
        }

    def stop(self):
        self._sensors.cleanup()
        super(WorkerThread, self).stop()

