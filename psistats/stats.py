'''
Created on Jun 21, 2014

@author: v0idnull
'''
import psutil
from netifaces import interfaces, ifaddresses, AF_INET
import socket
import os
from psistats import sensors
from psistats import hddtemp


def get_sensors(sensorList):
    sensors.init()

    deviceList = sensors.parse_config_list(sensorList)
    devices = sensors.iter_by_list(deviceList)

    sensors.cleanup()

    return devices

def get_hddspace(device):
    return psutil.disk_usage(device).percent

def get_hdds():
    disks = []
    for partition in psutil.disk_partitions():
        disks.append(partition.mountpoint)

    return disks

def get_hddtemps(ip, port):
    raw = hddtemp.get_hddtemp_from_network(ip, port)
    return hddtemp.parse_hddtemp(raw)


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    return None


def get_cpu(per_cpu=False):
    return psutil.cpu_percent(0, per_cpu)


def get_mem():
    vm = psutil.virtual_memory()
    return vm.percent


def get_ipaddrs_by_psutil():
    ifaces = psutil.net_if_addrs()
    ipaddrs = {}

    for interface in ifaces.iterkeys():
        if interface != "lo":
            for addr in ifaces[interface]:
                if addr.family == 2:
                    ipaddrs[interface] = addr.address
    return ipaddrs

def get_ipaddrs_by_netiface():
    ipaddrs = {}

    for interface in interfaces():

        if interface not in ipaddrs:
            ipaddrs[interface] = []

        links = ifaddresses(interface)

        if AF_INET in links:
            for link in links[AF_INET]:
                ipaddrs[interface].append(link['addr'])

    return ipaddrs

def get_ipaddrs():

    ipaddrs = {}

    try:
        ipaddrs = get_ipaddrs_by_psutil()
    except AttributeError:
        ipaddrs = get_ipaddrs_by_netiface()
    
    return ipaddrs



def get_hostname():
    return socket.gethostname()
