#!/usr/bin/env python

import sys
import os
import psutil
import time
import stat
import lockfile
import daemon
import argparse
from daemon import runner

from psistats import app
from psistats import config
from psistats import libsensors
from psistats.libsensors.lib.sensors import SensorsError

def get_args_parser():
    parser = argparse.ArgumentParser(description='Psistats')
    parser.add_argument('--version', action='store_true', help='Print out the version')
    parser.add_argument('--start', action='store_true', help='Start the psistats daemon')
    parser.add_argument('--stop', action='store_true', help='Stop the psistats daemon')
    parser.add_argument('--restart', action='store_true', help='Restart the psistats daemon')
    parser.add_argument('--start-console', action='store_true', help='Start psistats in console')
    parser.add_argument('--status', action='store_true', help='Get the status of the psistats daemon')
    parser.add_argument('--sensors', action='store_true', help='Get a list of the available sensors that psistats can use')
    parser.add_argument('--config', help='Location of configuration file')
    return parser




def init_context(config):
    out('LOADING CONTEXT\n')

    stream_stdout = open(config['app']['stdout_path'], 'w')
    stream_stderr = open(config['app']['stderr_path'], 'w')
    stream_pidfile = lockfile.FileLock(config['app']['pidfile'])

    context = daemon.DaemonContext(
        pidfile=stream_pidfile,
        stdout=stream_stdout,
        stderr=stream_stderr
    )
    return context

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


def start_local(args):
    """
    Starts psistats in the current terminal
    """
    out('[x] Starting Psistats service locally...\n')
    
    conf = config.get_config(args['config'])
    out('[x] Config file: %s\n' % conf.filename)

    psistatsApp = app.App(config.get_config())
    psistatsApp.start()
    

def start(args):
    """
    Starts psistats as a background service"
    """
    out('[x] Starting Psistats service... ')
    conf = config.get_config(args['config'])

    if is_running(conf['app']['pidfile']) == True:
        out("Already running!\n")
    else:
        newpid = os.fork()
        if newpid == 0:
            context = init_context(conf)
            context.open()

            psistatsApp = app.App(conf)
            psistatsApp.start()

            context.close()
            sys.exit()
        else:
            out("ok\n")
            out('[x] Config file %s\n' % conf.filename)

def stop(args):
    """
    Stop psistats
    """
    out('[x] Stopping Psistats service... ')
    psistats = app.App(config.get_config(args['config']))

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


def status(args):
    """
    Check if pidfile is a valid process"
    """
    psistats = app.App(config.get_config(args['config']))
    if is_running(psistats.pidfile_path) == True:
        sys.stdout.write("running\n")
    else:
        sys.stdout.write("not running\n")

def list_sensors(args):
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


def main(argv=None):

    if argv == None:
        argv = sys.argv

    parser = get_args_parser()
    args = vars(parser.parse_args(argv[1:]))

    print args

    retval = 0

    if 'start' in args and args['start'] == True:
        start(args)
    elif 'start_console' in args and args['start_console'] == True:
        start_local(args)
    elif 'stop' in args and args['stop'] == True:
        stop(args)
    elif 'restart' in args and args['restart'] == True:
        restart(args)
    elif 'status' in args and args['status'] == True:
        status(args)
    elif 'sensors' in args and args['sensors'] == True:
        list_sensors(args)

    return retval

if __name__ == "__main__":
    main(sys.argv)
