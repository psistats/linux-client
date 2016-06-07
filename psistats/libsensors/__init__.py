__all__ = ['sensors', 'config']

from psistats.libsensors.lib.sensors import init
from psistats.libsensors.lib.sensors import iter_detected_chips
from psistats.libsensors.lib.sensors import cleanup
from psistats.libsensors.lib.sensors import SENSORS_FEATURE_FAN
from psistats.libsensors.lib.sensors import SENSORS_FEATURE_TEMP
from psistats.libsensors.lib.sensors import SensorsError


class CantReadSensor(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Sensors():

    def __init__(self):
        self.chips = {}
        self.initted = False

    def init(self):
        init()
        self.initted = True

    def cleanup(self):
        cleanup()
        self.initted = False
    
    def add_chip(self, chipName):

        for chip in iter_detected_chips(chip_name=chipName):
            self.chips[chipName] = {}

            for feature in chip:
                print "feature label: %s" % feature.label
                self.chips[chipName][feature.label] = feature

    def _get_unit(self, feature):
        if feature.type == SENSORS_FEATURE_FAN:
            return 'rpm'
        elif feature.type == SENSORS_FEATURE_TEMP:
            return 'c'
        else:
            return None


    def get_value(self, chipName, featureLabel):

        try:
            if chipName in self.chips:
                if featureLabel in self.chips[chipName]:
                    feature = self.chips[chipName][featureLabel]
                    
                    return (feature.get_value(), self._get_unit(feature))
        except SensorsError as e:
            if e.message == "Can't read":
                raise CantReadSensor(featureLabel)
