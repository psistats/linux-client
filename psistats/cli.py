#!/usr/bin/env python

import sys
import os
import psutil
import time
import stat

from daemon import runner

from psistats import app
from psistats import config
from psistats import libsensors
from psistats.libsensors.lib.sensors import SensorsError

def out(msg):
    """
    Ensure messages are printed to stdout immediate"
    """
    sys.stdout.write(msg)
    sys.stdout.flush()


def is_running(pidfile):
    """
    Check if pidfile is a valid process
    """
    try:
        f = open(pidfile)
        pid = f.read()
        if psutil.pid_exists(int(pid)) == True:
            return True
        else:
            return False
    except:
        return False


def start_local():
    """
    Starts psistats in the current terminal
    """
    out('[x] Starting Psistats service locally... ')
    psistatsApp = app.App(config.get_config())
    psistatsApp.run()    
    

def start():
    """
    Starts psistats as a background service"
    """
    out('[x] Starting Psistats service... ')
    psistatsApp = app.App(config.get_config())

    if is_running(psistatsApp.pidfile_path) == True:
        out("Already running!\n")
    else:
        newpid = os.fork()

        if newpid == 0:
            daemon_runner = runner.DaemonRunner(psistatsApp)
            daemon_runner.do_action()

            sys.exit()
        else:
            out("ok\n")

def stop():
    """
    Stop psistats
    """
    out('[x] Stopping Psistats service... ')
    psistats = app.App(config.get_config())

    if (os.path.isfile(psistats.pidfile_path)):

        with open(psistats.pidfile_path) as f:
            pid = int(f.read())

            while True:
                out('.')
                try:
                    os.kill(pid, 9)
                except OSError:
                    pass

                if psutil.pid_exists(pid):
                    time.sleep(1)
                else:
                    break
        out("ok\n")
    else:
        out("ok\n")


def status():
    """
    Check if pidfile is a valid process"
    """
    psistats = app.App(config.get_config())
    if is_running(psistats.pidfile_path) == True:
        sys.stdout.write("running\n")
    else:
        sys.stdout.write("not running\n")

def list_sensors():
    """
    List available sensors in a config file format
    """
    libsensors.init()

    try:
        for chip in libsensors.iter_detected_chips():
            confKey = str(chip)

            unit = ''

            for feature in chip:
                if feature.type == libsensors.SENSORS_FEATURE_FAN:
                    unit = 'RPM'
                elif feature.type == libsensors.SENSORS_FEATURE_TEMP:
                    unit = '*C'
               
                v = None
                try:
                    v = feature.get_value()
                except SensorsError:
                    v = 'can not read this sensor'

                sys.stdout.write('%s.%s  (%s %s)\n' % (confKey, feature.label, v, unit))
    finally:
        libsensors.cleanup()


def help():
    sys.stdout.write('psistats [start|start-local|stop|restart|status|sensors]\n')

def main(argv=None):

    if argv == None:
        argv = sys.argv

    retval = 0
    
    if len(argv) != 2:
        help()
        retval = 1
    elif sys.argv[1] == 'start':
        start()
    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'restart':
        stop()
        start()
    elif sys.argv[1] == 'status':
        status()
    elif sys.argv[1] == 'start-local':
        start_local()
    elif sys.argv[1] == 'sensors':
        list_sensors()
    else:
        sys.stdout.write("psistats [start|start-local|stop|restart|status|sensors]\n")
        retval = 1

    return retval

if __name__ == "__main__":
    main()
