from setuptools import Command
import shutil, fnmatch, os

class CleanCommand(Command):

    description = "REMOVE ALL THE DAMN JUNK"

    buildFiles = [
        'target',
        'build',
        'dist',
        'psistats_client.egg-info',
        '3rdparty/sensors/build',
        '3rdparty/sensors/PySensors.egg-info',
        '.eggs'
    ]

    testFiles = [
        'coverage.xml',
        'htmlcov',
        '.cache',
        'tests/__pycache__'
        '.coverage'
    ]

    user_options = [
        ('all', 'a', 'Remove all junk'),
        ('build', 'b', 'Remove all build-related junk'),
        ('pyc', 'p', 'Remove all compiled python junk'),
        ('tests', 't', 'Remove all test/coverage junk')
    ]

    boolean_options = ['all','build','pyc','tests']

    def initialize_options(self):
        self.all = False
        self.build = False
        self.pyc = False
        self.tests = False

    def finalize_options(self):
        pass

    def _remove_files(self, files):
        for fn in files:
            print('CLEANING JUNK: %s' % fn)

            try:
                if os.path.isfile(fn):
                    os.remove(fn)
                else:
                    shutil.rmtree(fn)
            except OSError:
                pass

    def run(self):
        if self.all or self.tests:
            self._remove_files(self.testFiles)

        if self.all or self.build:
            self._remove_files(self.buildFiles)

        if self.all or self.pyc:
            for root, dirname, filenames in os.walk('.'):
                for filename in fnmatch.filter(filenames, '*.pyc'):
                    pycFile = os.path.join(root, filename)
                    print('CLEANING JUNK: %s' % pycFile)
                    os.remove(pycFile)

