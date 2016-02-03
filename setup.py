from setuptools import setup
from setuptools import Command
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import subprocess
import sys
import os
import inspect
import shutil

class CleanCmd(Command):

    """setuptools command"""

    description = "Cleanup Duty"
    user_options = []

    cleanDirs = [
        '.eggs',
        'build',
        'dist',
        'psistats_client.egg-info'
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
                shutil.rmtree(dirName)
            except OSError:
                pass

def install_3rdparties():

    libDir = os.path.dirname(os.path.realpath(__file__)) + '/3rdparty'
    cwd = os.getcwd()

    deps = ['sensors']
    for dep in deps:
        depDir = libDir + '/' + dep
        os.chdir(depDir)
        p = subprocess.Popen(['python', 'setup.py', 'install'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (stdoutdata,stderrdata) = p.communicate()

        sys.stdout.write(stdoutdata)
        sys.stdout.flush()
        os.chdir(cwd)



class install(_install):
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

class develop(_develop):
    def run(self):
        _develop.run(self)
        self.execute(install_3rdparties, [], msg="INSTALLING 3rd PARTIES")


setup(
    name="psistats-client",
    version="0.1.1dev0",
    description="Psistats python client",
    url="http://psistats.psikon.org",
    author="Alex D",
    author_email="adow@psikon.com",
    license="MIT",
    packages=['psistats'],
    data_files=[('share/psistats', ['psistats.conf'])],
    zip_safe=False,
    test_suite="tests",
    tests_require=[
        'mock',
        'coverage'
    ],
    install_requires=[
        'pika',
        'python-daemon',
        'simplejson',
        'netifaces',
        'psutil',
        'clint'
    ],
    scripts=[
        'bin/psistats'
    ],
    cmdclass={
        'install': install,
        'develop': develop,
        'clean': CleanCmd
    }
#    entry_points={
#        'distutils.commands': [
#            'clean = cleanCmd'
#        ]
#    }
)
