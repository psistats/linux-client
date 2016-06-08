import psutil
from psistats.hdd import hddtemp

def get_hdd_space(device):
    return psutil.disk_usage(device).percent

def get_hdds():
    disks = []
    for partition in psutil.disk_partitions():
        disks.append(partition.mountpoint)

    return disks

def get_hdd_temps(ip, port):
    raw = hddtemp.get_hddtemp(ip, port)
    return hddtemp.parse_hddtemp(raw)
