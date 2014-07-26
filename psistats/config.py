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
from psistats.exceptions import FileNotFoundException
import ConfigParser

config_file = "psistats.conf"


class Config(object):

    def __init__(self, filename):

        rawconfig = ConfigParser.RawConfigParser()
        rawconfig.read(filename)

        config = {}

        for section in rawconfig.sections():
            config[section] = self._process_section(rawconfig.items(section))

        self._config = config
        self._config['logging'] = self._logging_config()

    def _process_section(self, section):

        d = {}

        for key, val in section:
            if val.lower() == 'false' or val.lower() == 'no':
                val = False
            elif val.lower() == 'true' or val.lower() == 'yes':
                val = True
            elif val.isdigit() == True:
                val = int(val)

            d[key] = val

        return d

    def __getitem__(self, name):
        return self._config[name]

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


def get_config():
    return Config(filename=get_config_file())


def get_config_file():

    system = platform.system()

    if system == "Linux":
        return get_linux_config_file()
    else:
        raise RuntimeError("System not supported")


def get_homedir_config_file():
    user_dir = os.path.expanduser("~")
    return user_dir + '/.psistats/' + config_file


def get_linux_config_file():

    cwd = os.getcwd()

    if os.path.isfile(cwd + "/" + config_file):
        return cwd + "/" + config_file
    elif os.path.isfile(get_homedir_config_file()):
        return get_homedir_config_file()
    elif os.path.isfile("/etc/" + config_file):
        return "/etc/" + config_file

    raise FileNotFoundException("No config file was found")
