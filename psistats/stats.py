'''
Created on Jun 21, 2014

@author: v0idnull
'''
import psutil
from netifaces import interfaces, ifaddresses, AF_INET
import socket
import os

def cpu_temp_acpi_parser(input):
    return input.strip().lstrip('temperature :').rstrip('c')

def cpu_temp_device_parser(input):
    return float(input) / 1000.0

cpu_temp_callbacks = {
    "/proc/acpi/thermal_zone/THM0/temperature": cpu_temp_acpi_parser,
    "/proc/acpi/thermal_zone/THRM/temperature": cpu_temp_acpi_parser,
    "/proc/acpi/thermal_zone/THR1/temperature": cpu_temp_acpi_parser,
    "/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp": cpu_temp_device_parser,
    "/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp": cpu_temp_device_parser,
    "/sys/class/thermal/thermal_zone0/temp" : cpu_temp_device_parser
}

def cpu_temp():
    for key in cpu_temp_callbacks:
        if (os.path.exists(key)):
            return cpu_temp_callbacks[key](open(key).read())
    

def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds


def cpu(per_cpu=False):
    return psutil.cpu_percent(0, per_cpu)


def mem():
    vm = psutil.virtual_memory()
    return vm.percent


def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        if interface not in ['virbr0']:
            addrs = ifaddresses(interface)
            if AF_INET in addrs:
                for link in addrs[AF_INET]:
                    if (link['addr'] != '127.0.0.1'):
                        ip_list.append(link['addr'])
    return ip_list


def hostname():
    return socket.gethostname()
