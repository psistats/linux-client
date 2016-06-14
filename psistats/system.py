import psutil
import platform

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    return None


def get_cpu_usage(per_cpu=False):
    return psutil.cpu_percent(0, per_cpu)


def get_mem_usage():
    vm = psutil.virtual_memory()
    return vm.percent


def get_distro():
    try:
        linux = platform.linux_distribution()
        return "%s %s" % (linux[0], linux[1])
    except:
        return "%s %s" % (platform.system(), platform.release())

