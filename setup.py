from setuptools import setup
from setuptools import Command
import subprocess
import sys
import os
import inspect
import shutil
import fnmatch

from buildcmds.clean import CleanCommand

setup(
    name="psistats",
    version="0.1.1develop",
    description="Psistats python client",
    url="http://github.com/alex-dow/psistats-linux-client",
    author="Alex D",
    author_email="adow@psikon.com",
    license="MIT",
    packages=['psistats', 'psistats.sensors'],
    package_dir={
        'psistats': 'lib/psistats', 
        'psistats.sensors': 'lib/psistats/sensors' 
    },
    data_files=[('share/psistats', ['psistats.conf'])],
    zip_safe=False,
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest-cov',
        'mock==1.0.1',
        'pytest'
    ],
    install_requires=[
        'pika',
        'python-daemon',
        'simplejson',
        'psutil',
        'netifaces'
    ],
    entry_points={
        'console_scripts': [
            'psistats = psistats.cli:main'
        ]
    },
    cmdclass={
        'clean': CleanCommand,
    }
)
