from setuptools import setup
from setuptools import Command
import subprocess
import sys
import os
import inspect
import shutil
import fnmatch

from buildcmds.pytest import PyTest
from buildcmds.clean import CleanCommand

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


setup(
    name="psistats",
    version="0.1.1develop",
    description="Psistats python client",
    url="http://github.com/alex-dow/psistats-linux-client",
    author="Alex D",
    author_email="adow@psikon.com",
    license="MIT",
    packages=['psistats', 'psistats/sensors'],
    data_files=[('share/psistats', ['psistats.conf'])],
    zip_safe=False,
    setup_requires=[
        'pytest'
    ],
    tests_require=[
        'PyTest',
        'pytest-cov',
        'mock==1.0.1'
    ],
    install_requires=[
        'pika',
        'python-daemon',
        'simplejson',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'psistats = psistats.cli:main'
        ]
    },
    cmdclass={
        'clean': CleanCommand,
        'test': PyTest
    }
)
