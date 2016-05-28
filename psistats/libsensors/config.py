def parse_config_list(sensorList):
    devices = {}

    deviceFilter = {}

    for device in sensorList:

        if device.startswith('('):
            parts = device.split(',')
            label = ','.join(parts[:-1]).strip()[1:]
            device = parts[-1:][0][:-1].strip()
        else:
            label = device

        devices[label] = { 
            'value': None,
            'unit': None
        }   

        chipName,feature = device.split('.')

        if chipName not in deviceFilter:
            deviceFilter[chipName] = {}

        deviceFilter[chipName][feature] = label

    return deviceFilter 


