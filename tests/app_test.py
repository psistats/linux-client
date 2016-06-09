import unittest, mock
import os
from psistats.app import App
from psistats.config import Config

class FakeWorker():
    def __init__(*args, **kwargs):
        pass


def fake_get_hostname():
    return 'localhost'

def fake_loop_keyboardInterrupt():
    raise KeyboardInterrupt()

class AppTest(unittest.TestCase):

    def setUp(self):
        testdir = os.path.dirname(os.path.realpath(__file__))
        conffile = testdir + "/fixtures/test.conf"
        self.confobj = Config(conffile)

    @mock.patch('psistats.app.net.get_hostname', side_effect=fake_get_hostname)
    @mock.patch('psistats.app.App._loop')
    def test_run_noworkers(self, gh, lp):
        a = App(self.confobj)
        a.start()

        self.assertEqual(a.isRunning(), True)
        self.assertEqual(a.config['queue']['name'], 'psistats.localhost')
        self.assertEqual(lp.called, True)
    
    @mock.patch('psistats.app.App._loop')
    def test_run_mixedWorkers(self, lp):
        a = App(self.confobj)
        a.reporters.append(('enabled_reporter', FakeWorker))
        a.reporters.append(('disabled_reporter', FakeWorker))

        a.start()
        self.assertIsInstance(a._reporterThreads['enabled_reporter'], FakeWorker)
        self.assertEqual('disabled_reporter' in a._reporterThreads, False)

    @mock.patch('psistats.app.App._loop', side_effect=fake_loop_keyboardInterrupt)
    def test_keyboardInterrupt(self, lp):
        a = App(self.confobj)

        with mock.patch.object(App, 'stop', wraps=a.stop) as mockStop:
            a.start()

            self.assertEqual(a.isRunning(), False)
            self.assertEqual(mockStop.called, True) 
