'''
Created on Jun 21, 2014

@author: v0idnull
'''
import psutil
# from netifaces import interfaces, ifaddresses, AF_INET
import socket
import os
from psistats.sensors import sensors as libsensors


def sensors(sensorList):
    libsensors.init()

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

    for chipName in deviceFilter.iterkeys():
        for chip in libsensors.iter_detected_chips(chip_name=chipName):
            for feature in chip:
                if feature.label in deviceFilter[chipName]:
                    unit = None
                    if feature.type == libsensors.SENSORS_FEATURE_FAN:
                        unit = 'RPM'
                    elif feature.type == libsensors.SENSORS_FEATURE_TEMP:
                        unit = 'C'

                    devices[deviceFilter[chipName][feature.label]]['value'] = feature.get_value()
                    devices[deviceFilter[chipName][feature.label]]['unit'] = unit

    libsensors.cleanup()

    return devices

def hddspace(device):
    return psutil.disk_usage(device).percent

def hdds():
    disks = []
    for partition in psutil.disk_partitions():
        disks.append(partition.mountpoint)

    return disks

def hddtemps(ip, port):
    s = socket.socket()
    s.connect((ip, port))
    buf = s.recv(2048)

    hddtemps = {}
    
    buf = buf[1:]
    
    devices = buf.split('||')
    for device in devices:
        parts = device.split('|')

        hddtemps[parts[0]] = {
            'value': parts[2],
            'unit': parts[3]
        }

    return hddtemps


def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    return None


def cpu(per_cpu=False):
    return psutil.cpu_percent(0, per_cpu)


def mem():
    vm = psutil.virtual_memory()
    return vm.percent


def ipaddr():

    ifaces = psutil.net_if_addrs()
    ipaddrs = {}

    for interface in ifaces.iterkeys():
        if interface != "lo":
            for addr in ifaces[interface]:
                if addr.family == 2:
                    ipaddrs[interface] = addr.address
    return ipaddrs


def hostname():
    return socket.gethostname()
