__all__ = ['sensors', 'config']

from psistats.libsensors.lib.sensors import init
from psistats.libsensors.lib.sensors import iter_detected_chips
from psistats.libsensors.config import parse_config_list
from psistats.libsensors.lib.sensors import cleanup
from psistats.libsensors.lib.sensors import SENSORS_FEATURE_FAN
from psistats.libsensors.lib.sensors import SENSORS_FEATURE_TEMP


def iter_by_list(sensorList):
    devices = {}
    for chipName in sensorList.iterkeys():
        for chip in iter_detected_chips(chip_name=chipName):
            for feature in chip:
                if feature.label in sensorList[chipName]:
                    unit = None
                    if feature.type == SENSORS_FEATURE_FAN:
                        unit = 'RPM'
                    elif feature.type == SENSORS_FEATURE_TEMP:
                        unit = 'C' 

                    if sensorList[chipName][feature.label] not in devices:
                        devices[sensorList[chipName][feature.label]] = {'value': None, 'unit': None}

                    devices[sensorList[chipName][feature.label]]['value'] = feature.get_value()
                    devices[sensorList[chipName][feature.label]]['unit'] = unit

    return devices

