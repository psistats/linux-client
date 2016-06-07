import unittest
import mock
import os

from psistats import config

class ConfigParseTest(unittest.TestCase):
    def setUp(self):

        testdir = os.path.dirname(os.path.realpath(__file__)) + "/.."

        conffile = testdir + "/fixtures/test.conf"

        self.confobj = config.get_config(config_file=conffile)

    def test_parse_boolean(self):

        self.assertEqual(self.confobj['enabled_reporter']['enabled'], True)
        self.assertEqual(self.confobj['disabled_reporter']['enabled'], False)

    def test_parse_sensors(self):

        self.assertEqual(self.confobj['sensors']['devices']['chipName1']['featureName1'], 'Label1')
        self.assertEqual(self.confobj['sensors']['devices']['chipName2']['featureName2'], 'Label2')

    def test_parse_logging(self):

        expected = {
            'root': {
                'qualname': 'psistats', 
                'level': 'DEBUG', 
                'propagate': 0, 
                'handlers': ['fileout', 'stdout']
            }, 
            'version': 1, 
            'loggers': {
                'pika': {
                    'level': 'DEBUG',
                    'handlers': ['fileout','stdout'],
                    'propagate': 0,
                    'qualname': 'pika'
                }
            },
            'formatters': {
                'form1': {
                    'format': 'some_custom_format', 
                    'class': 'logging.Formatter'
                }
            }, 
            'handlers': {
                'fileout': {
                    'formatter': 'form1', 
                    'filename': 'psistats.log', 
                    'when': 'midnight', 
                    'class': 'logging.handlers.TimedRotatingFileHandler', 
                    'level': 'INFO'
                }, 
                'stdout': {
                    'level': 'DEBUG', 
                    'formatter': 'form1', 
                    'class': 'logging.StreamHandler', 
                    'stream': 'ext://sys.stdout'
                }
            }
        }   
       
        self.assertEqual(self.confobj['logging'], expected)

