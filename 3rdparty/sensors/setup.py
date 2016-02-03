#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sensors

setup(
    name='PySensors',
    version=sensors.__version__,
    author=sensors.__author__,
    author_email=sensors.__contact__,
    packages=['sensors'],
    #scripts=[],
    url='http://pypi.python.org/pypi/PySensors/',
    #download_url='',
    license=sensors.__license__,
    description='Python bindings to libsensors (via ctypes)',
    keywords=['sensors', 'hardware', 'monitoring'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved ::'
        ' GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
    ]
)

