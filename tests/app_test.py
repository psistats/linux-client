import unittest, mock
import os, sys
from psistats.app import App
from psistats.config import Config

class FakeWorker():
    def __init__(self, *args, **kwargs):
        self._running = False

    def start(self):
        self.run()

    def run(self):
        self._running = True

    def stop(self):
        self._running = False

    def running(self):
        return self._running


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
    @mock.patch('psistats.app.App.isRunning', side_effect=False)
    def test_queue_setup(self, gh, lp):
        a = App(self.confobj)
        a.start()

        self.assertEqual(a.config['queue']['name'], 'psistats.localhost')
    
    @mock.patch('psistats.app.App.isRunning', side_effect=False)
    def test_run_mixedWorkers(self, lp):
        a = App(self.confobj)
        a.reporters.append(('enabled_reporter', FakeWorker))
        a.reporters.append(('disabled_reporter', FakeWorker))

        a.start()
        self.assertIsInstance(a._reporterThreads['enabled_reporter'], FakeWorker)
        self.assertEqual('disabled_reporter' in a._reporterThreads, False)

    @mock.patch('psistats.app.App.work', side_effect=fake_loop_keyboardInterrupt)
    def test_keyboardInterrupt(self, lp):
        a = App(self.confobj)

        with mock.patch.object(App, 'stop', wraps=a.stop) as mockStop:
            a.start()

            self.assertEqual(a.isRunning(), False)
            self.assertEqual(mockStop.called, True)

    @mock.patch('psistats.app.App.stop')
    @mock.patch('psistats.app.time.sleep')
    def test_startThreads(self, stop, mockTimeSleep):
        a = App(self.confobj)
        a.reporters.append(('enabled_reporter', FakeWorker))


        class MockIsRunning(object):

            def __init__(self, app):
                self.running = False
                self.iteration = 0
                self.app = app
                self.threadRan = False

            def __call__(self):
                self.iteration += 1

                if self.iteration == 2:
                    sys.stdout.write('ITERATION #2\n')
                    self.threadRan = self.app._reporterThreads['enabled_reporter'].running()
                    return False
                else:
                    sys.stdout.write('ITERATION #1\n')
                    return True

        mockIsRunning = MockIsRunning(a)

        with mock.patch.object(a, 'isRunning', side_effect=mockIsRunning):
            a.reporters.append(('enabled_reporter', FakeWorker))
            a.start()
            
        assert mockIsRunning.threadRan == True

