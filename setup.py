from setuptools import setup

setup(
    name="psistats",
    version="0.0.4",
    description="Psistats python client",
    url="http://psistatsold.psikon.org",
    author="Alex Dowgailenko",
    author_email="v0idnull@gmail.com",
    license="MIT",
    packages=['psistats','psistats.app'],
    data_files=[('scripts', ['bin/psistats-service']), ('config', ['psistats.conf'])],
    zip_safe=False,
    install_requires=[
        'pika',
        'python-daemon',
        'simplejson',
        'netifaces',
        'psutil'
    ],
    scripts=['bin/psistats']
)
