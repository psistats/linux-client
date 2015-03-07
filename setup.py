from setuptools import setup

setup(
    name="psistats-client",
    version="0.1.0.1-dev",
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
        'mock>=1.0.1',
        'coverage>=3.7.0'
    ],
    install_requires=[
        'pika>=0.9.14',
        'python-daemon>=1.5.5',
        'simplejson>=3.6.3',
        'netifaces>=0.10.4',
        'psutil>=2.1.1'
    ],
    scripts=[
        'bin/psistats',
    ]
)
