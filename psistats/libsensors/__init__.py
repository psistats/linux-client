from psistats.libsensors.lib.sensors import init
from psistats.libsensors.lib.sensors import iter_detected_chips
from psistats.libsensors.lib.sensors import cleanup
from psistats.libsensors.lib.sensors import SENSORS_FEATURE_FAN
from psistats.libsensors.lib.sensors import SENSORS_FEATURE_TEMP
from psistats.libsensors.lib.sensors import SensorsError

__all__ = ['Sensors', 'CantReadSensor']

class CantReadSensor(Exception):
    """Thrown when a sensor can not be read"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Sensors():
    
    def __init__(self):
        self.chips = {}
        self.initted = False

    def init(self):
        """Initialize sensors"""
        init()
        self.initted = True

    def cleanup(self):
        """Cleanup after using sensors"""
        cleanup()
        self.initted = False
    
    def add_chip(self, chipName):
        """Add a chip"""
        for chip in iter_detected_chips(chip_name=chipName):
            self.chips[chipName] = {}

            for feature in chip:
                self.chips[chipName][feature.label] = feature

    def _get_unit(self, feature):
        if feature.type == SENSORS_FEATURE_FAN:
            return 'rpm'
        elif feature.type == SENSORS_FEATURE_TEMP:
            return 'c'
        else:
            return None


    def get_value(self, chipName, featureLabel):
        """Get a value of a specific feature from a chip"""
        try:
            if chipName in self.chips:
                if featureLabel in self.chips[chipName]:
                    feature = self.chips[chipName][featureLabel]
                    
                    return (feature.get_value(), self._get_unit(feature))
        except SensorsError as e:
            if str(e) == "Can't read":
                raise CantReadSensor(featureLabel)
