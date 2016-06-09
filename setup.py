from setuptools import setup

setup(
    name="psistats",
    version="0.2.0develop",
    description="Psistats Reporting Client",
    long_description="A python tool to report computer vitals to an amqp message queue",
    url="http://github.com/alex-dow/psistats-linux-client",
    author="Alex Dowgailenko",
    author_email="adow@psikon.com",
    license="MIT",
    packages=['psistats', 'psistats.libsensors', 'psistats.libsensors.lib', 'psistats.hdd', 'psistats.workers'],
    platforms=['unix','linux'],
    package_dir={
        'psistats': 'psistats', 
        'psistats.hdd': 'psistats/hdd',
        'psistats.libsensors': 'psistats/libsensors',
        'psistats.libsensors.lib': 'psistats/libsensors/lib',
        'psistats.workers': 'psistats/workers'
    },
    data_files=[('etc', ['etc/psistats.conf'])],
    zip_safe=False,
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
        'netifaces',
        'lockfile'
    ],
    scripts=[
        'bin/psistats'
    ],
    options={
        'build_scripts': {
            'executable': '/usr/bin/env python'
        }
    }
)
