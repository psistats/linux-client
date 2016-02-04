from setuptools import setup
from setuptools import Command
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import subprocess
import sys
import os
import inspect
import shutil
import fnmatch


def writeStdout(msg):
    if sys.version_info < (3,):
        sys.stdout.write(msg)
    else:
        sys.stdout.buffer.write(msg)

def executeShellCmd(cmd, cwd=None):
    oldcwd = None
    
    if cwd != None:
        oldcwd = os.getcwd()
        os.chdir(cwd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while p.poll() is None:
        writeStdout(p.stdout.readline())

    (stdoutdata,stderrdata) = p.communicate()

    writeStdout(stdoutdata)

    if cwd != None:
        os.chdir(oldcwd)

    return p.returncode


def installDependency(dep):
    cmd = ['pip','install'] + dep

    print(cmd)

    ret = executeShellCmd(cmd)

    if ret != 0 and ret != 2:
        raise RuntimeError('Failed to install dependencies! Return code: %s' % ret)


def install_3rdparties():

    libDir = os.path.dirname(os.path.realpath(__file__)) + '/3rdparty'
    cwd = os.getcwd()

    deps = ['sensors']
    for dep in deps:
        depDir = libDir + '/' + dep
        ret = executeShellCmd(['python','setup.py','install'], depDir)

        if ret > 0:
            raise RuntimeError('Could not install 3rd party library: %s' % dep)


class CleanCommand(Command):

    """setuptools command"""

    description = "Cleanup Duty"
    user_options = []

    cleanDirs = [
        'coverage.xml',
        'htmlcov',
        '.cache',
        '.eggs',
        'build',
        'dist',
        'psistats_client.egg-info',
        '3rdparty/sensors/build',
        '3rdparty/sensors/dist',
        '3rdparty/sensors/PySensors.egg-info',
        '.coverage',
        'tests/__pycache__'
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print('Cleaning build-related junk')
        for dirName in self.cleanDirs:
            print( 'Deleting %s' % dirName)
            try:
                if os.path.isfile(dirName):
                    os.remove(dirName)
                else:
                    shutil.rmtree(dirName)
            except OSError:
                pass
        print('Cleaning pyc files')
        for root, dirname, filenames in os.walk('.'):
            for filename in fnmatch.filter(filenames, '*.pyc'):
                pycFile = os.path.join(root, filename)
                print('Deleting %s' % pycFile)
                os.remove(pycFile)


class InstallCommand(_install):
    def run(self):
         # Explicit request for old-style install?  Just do it
        if self.old_and_unmanageable or self.single_version_externally_managed:
            return orig.install.run(self)

        if not self._called_from_setup(inspect.currentframe()):
            # Run in backward-compatibility mode to support bdist_* commands.
            orig.install.run(self)
        else:
            self.do_egg_install()
       
        self.execute(install_3rdparties, [], msg="INSTALLING 3rd PARTIES")


class DevelopCommand(_develop):
    def run(self):
        _develop.run(self)
        self.execute(install_3rdparties, [], msg="INSTALLING 3rd PARTIES")


class CoverageCommand(Command):
    description = "Create coverage reports"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        installDependency(['mock','coverage','pytest','pytest-cov'])

        cmd = [
            'py.test',
            '--cov-report',
            'html',
            '--cov-report',
            'xml',
            '--cov',
            'psistats',
            'tests/'
        ]

        ret = executeShellCmd(cmd)
        if ret > 0:
            raise RuntimeError('Unable to run coverage reports, error code: %s ' % ret)


class TestCommand(Command):
    description = "Run unit tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        installDependency(['mock','coverage','pytest'])

        ret = executeShellCmd(['py.test', '--verbose', 'tests/'])
        if ret > 0:
            raise RuntimeError('Unable to run unit tests')


setup(
    name="psistats-client",
    version="0.1.1dev0",
    description="Psistats python client",
    url="http://github.com/alex-dow/psistats-linux-client",
    author="Alex D",
    author_email="adow@psikon.com",
    license="MIT",
    packages=['psistats'],
    data_files=[('share/psistats', ['psistats.conf'])],
    zip_safe=False,
    test_suite="tests",
    tests_require=[
        'pytest',
        'mock',
        'coverage',
        'pytest-cov'
    ],
    install_requires=[
        'pika',
        'python-daemon',
        'simplejson',
        'gns3-netifaces',
        'psutil',
        'clint'
    ],
    scripts=[
        'bin/psistats'
    ],
    cmdclass={
        'install': InstallCommand,
        'develop': DevelopCommand,
        'clean': CleanCommand,
        'coverage': CoverageCommand,
        'test': TestCommand
    }
)
