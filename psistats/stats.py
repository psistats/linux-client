'''
Created on Jun 21, 2014

@author: v0idnull
'''
import psutil
from netifaces import interfaces, ifaddresses, AF_INET
import socket


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
