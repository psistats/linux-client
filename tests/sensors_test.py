import unittest
import mock

import os
import sys

from psistats.libsensors.lib.sensors import SensorsError
from psistats.libsensors import CantReadSensor


class MockFeatureOne():
    def get_value(self):
        raise SensorsError(message='Can\'t read')

class MockFeatureTwo():
    def __init__(self):
        self.type = 0x01

    def get_value(self):
        return 1

class MockFeatureThree():
    def __init__(self):
        self.type = 0x02

    def get_value(self):
        return 2
    

class SensorsTest(unittest.TestCase):

    def test_cant_read_exception(self):
        from psistats.libsensors import Sensors

        s = Sensors()
        
        s.chips['fakechip'] = {'fakefeature': MockFeatureOne()}
        
        self.assertRaises(CantReadSensor, s.get_value, 'fakechip', 'fakefeature')


