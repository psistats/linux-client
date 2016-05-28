import psutil
from netifaces import interfaces, ifaddresses, AF_INET
import socket
import os

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
