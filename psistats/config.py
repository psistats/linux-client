###############################################################################
# Psistats Configuration                                                      #
#                                                                             #
# Version 0.0.1                                                               #
# MIT License                                                                 #
# v0idnull                                                                    #
# http://www.psikon.com/                                                      #
###############################################################################
import os
import platform
from psistats.exceptions import *

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

CONF_FILE = "psistats.conf"

class Config(object):

    def __init__(self, filename):
        if os.path.isfile(filename) == False:
            raise FileNotFoundException(filename)

        rawconfig = configparser.RawConfigParser()
        rawconfig.read(filename)

        config = {}

        for section in rawconfig.sections():
            config[section] = self._process_section(rawconfig.items(section))

        self._config = config
        self._config['logging'] = self._logging_config()

        self.filename = filename

    def _process_section(self, section):

        d = {}

        for key, val in section:
            if val.lower() == 'false' or val.lower() == 'no':
                val = False
            elif val.lower() == 'true' or val.lower() == 'yes':
                val = True
            elif val.isdigit() == True:
                val = int(val)

            if key.endswith('[]'):
                key = key[:-2]
                val = map(lambda x: x.strip(), val.split('\n'))
                
            d[key] = val

        return d

    def __getitem__(self, name):
        if name in self._config:
            return self._config[name]
        else:
            raise KeyError(name)

    def __contains__(self, name):
        return name in self._config

    def _logging_config(self):
        log_keys = self['logging']
        hand_keys = self['handlers']
        form_keys = self['formatters']

        loggers = {}
        handlers = {}
        formatters = {}

        for logger_name in log_keys['keys'].split(','):
            lname = 'logger_' + logger_name

            section = self[lname]

            for i in section:
                if i == 'handlers':
                    section['handlers'] = section['handlers'].split(',')

            if logger_name == 'root':
                root_logger = section
            else:
                loggers[logger_name] = section

        for i in hand_keys['keys'].split(','):
            hname = 'handler_' + i
            handlers[i] = self[hname]

        for i in form_keys['keys'].split(','):
            fname = 'formatter_' + i
            formatters[i] = self[fname]

        return {
            'version': 1,
            'formatters': formatters,
            'handlers': handlers,
            'loggers': loggers,
            'root': root_logger
        }


def get_config(config_file=None):
    if config_file == None:
        return Config(filename=get_config_file())
    else:
        return Config(filename=config_file)


def get_config_file():

    system = platform.system()

    if system == "Linux":
        return get_linux_config_file()
    else:
        raise PsistatsException("System not supported: %s" % system)


def get_homedir_config_file():
    user_dir = os.path.expanduser("~")
    return user_dir + '/.psistats/' + CONF_FILE


def get_linux_config_file():

    cwd = os.getcwd()

    if os.path.isfile(cwd + "/" + CONF_FILE):
        return cwd + "/" + CONF_FILE
    elif os.path.isfile(get_homedir_config_file()):
        return get_homedir_config_file()
    elif os.path.isfile("/etc/psistats/" + CONF_FILE):
        return "/etc/psistats/" + CONF_FILE
    elif os.path.isfile('/usr/local/share/psistats/' + CONF_FILE):
        return '/usr/local/share/psistats/' + CONF_FILE
    elif os.path.isfile('/usr/share/psistats/' + CONF_FILE):
        return '/usr/share/psistats/' + CONF_FILE

    raise FileNotFoundException("Unable to find configuration file %s" % CONF_FILE)
