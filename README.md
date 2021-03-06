Psistats Linux Client
=====================

Python linux client that sends computer statistics to an AMQP-compatible message queue.

Version 0.2.0 is currently in alpha. Features or functionality may change. Assume bugs exist.

Purpose
-------

There are a wide variety of reporting tools that can report any number of statistics in some form or fashion. The problem with most of them is that they tend to be bundled within larger sys admin tool sets, offer persistance of reports when you may not want them, or otherwise contain any number of features you may not want.

Psistats attempts to separate reporting into it's own isolated service. By sending data to a message queue, any number of applications that consume the reports can be made separately, including storing information into databases, sending alerts, wall displays, etc.

If you are looking for an all-in-one solution to reporting, this may not be the tool for you.
If you are looking for desktop widgets for one computer, then [Conky](https://github.com/brndnmtthws/conky) may be for you.

If you are looking to make custom, purpose-made displays to report details on one or more machines, then this tool fits this role perfectly.


Requirements
------------

1. Python 2.7 or Python 3.2+ (tested on Python 3.5)
2. An amqp server. Tested with [RabbitMQ](http://www.rabbitmq.com/)
3. If you want to report your various computer sensors, then you need libsensors installed
4. If you want to report the temperatures of your hard drive, then you need hddtemp installed and running as a server.


Installation (From Source):
---------------------------

1. $ python setup.py install
2. $ sudo ln -s /usr/bin/psistats bin/psistats
3. $ sudo cp etc/psistats /etc/psistats

Note, this won't start psistats on boot, but the exectuable is compatible with init scripts, upstart, etc.

Installation (Debian / Ubuntu):
-----------------------------------------------------------

Only snapshot builds are available at this time. To install the snapshot repository, run the following commands:

```
$ echo "deb http://debrepo.psikon.org/snapshots $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/psikon.list
$ sudo wget -O - http://debrepo.psikon.org/psikon.gpg.key | apt-key add -
$ sudo apt-get update
$ sudo apt-get install psistats
```

Psistats will automatically start on boot.


Usage
-----

After configuring psistats, you may start it in a console:

```
$ psistats start-local
```

Or you can start it in the background:

```
$ psistats start
```

Psistats will start sending messages to your message queue server right away. Each reporter sends its own messages on their own intervals. Refer to the configuration documentation below.

Messages are in JSON format. You can enable debug logging to see the JSON strings being sent.

Not all reporters need to be run at 1 second intervals. Running psistats in a console with debug logging enabled, you will be able to see if some reporter intervals can be increased.


Configuration
-------------

## General Settings

###Server Settings:

```
[server]
url=amqp://guest:guest@localhost:5672
```

* **url:** amqp url to your amqp server

WARNING: Users of older operating systems such as Ubuntu 14.04 have older system packages for pika (v0.9.13 or lower). If using these older versions, you must include a /%2f at the end of your url if you have no virtual host.

## Reporter Settings

###Sensors:

The sensors reporter can report information on any available sensor that libsensor can detect. You must have libsensor already installed.

To view a list of available sensors run:

```
$ psistats sensors
```


```
[sensors]
enabled=1
interval=1
devices[] = (CPU Core 1, coretemp-isa-0000.Core 0)
            (CPU Core 2, coretemp-isa-0000.Core 1)
            (CPU Core 3, coretemp-isa-0000.Core 2)
            (CPU Core 4, coretemp-isa-0000.Core 3)
```

* **enabled:** Turn reporter on or off
* **interval:** Number of seconds between reports
* **devices[]:** A list of label/sensor name

The list of devices are in the format of (LABEL, CHIP.FEATURE)


###HDD Temperature

Reports temperature data of your hard drives, if available. 

Requires hddtemp to be installed, and running as a daemon.

```
[hddtemp]
enabled=1
interval=30
hostname=127.0.0.1
port=7634
```

* **enabled:** Turn reporter on or off
* **interval:** Number of seconds between reports
* **hostname:** Host name or IP address of the hddtemp daemon
* **port:** Port number of the hddtemp daemon

###HDD Space

Reports total space used as a percentage for all available harddrives

```
[hddspace]
enabled=1
interval=60
```

* **enabled:** Turn reporter on or off
* **interval:** Number of seconds between reports

###IP Address

Reports all available IP addresses and device names

```
[ipaddr]
enabled=1
interval=60
```

* **enabled:** Turn reporter on or off
* **interval:** Number of seconds between reports

###Memory

Reports total memory usage in percent

```
[mem]
enabled=1
interval=1
```

* **enabled:** Turn reporter on or off
* **interval:** Number of seconds between reports

###CPU

Reports total cpu usage in percent, per core

```
[cpu]
enabled=1
interval=1
```

* **enabled:** Turn reporter on or off
* **interval:** Number of seconds between reports

###Uptime

Reports the system uptime

```
[cpu]
enabled=1
interval=1
```

* **enabled:** Turn reporter on or off
* **interval:** Number of seconds between reports


## Logging

Logging configuration is the python standard. You can read more about it at https://docs.python.org/2/library/logging.config.html#configuration-dictionary-schema.

Here is an example configuration that logs INFO level messages and above to a log file.

```
[logging]
keys=root

[handlers]
keys=fileout

[formatters]
keys=form1

[logger_root]
level=info
handlers=fileout
propagate=0
qualname=psistats

[handler_fileout]
class=logging.handlers.TimedRotatingFileHandler
filename=psistats.log
when=midnight
level=DEBUG
formatter=form1

[formatter_form1]
format=%(asctime)s %(name)s %(levelname)s %(message)s
class=logging.Formatter
```

Changelog
---------
v0.2.0
- New multithreaded (well, as mt as python can be) architecture
- Can interface with hddtemp and libsensors
- Can control timer for any reporter
- Various code improvements

v0.1.0
- Refactored entirely the interaction between psistats and RabbitMQ
- Enabled the ability to turn on or off any bit of information that is broadcasted
- Reorganized configuration file with comments
- Numerous code improvements
- Unit tests
- Better build scripts
 
v0.0.11
- Code improvements

v0.0.10
- Big version increase after testing automated release scripts
- Normalized configuration between linux and windows clients
- Fixed bug with pika 0.9.5 (default on ubuntu 12.04 systems)
- Some code clean up

v0.0.4
- Added cpu temperature
- Removed ping feature
- Message sending is now mandatory so if queue or exchange is removed, client will try to recreate the connection
- More sensible default logging parameters, including exposing pika-related logging
- Debian builds
- Various code clean up
- Removed the install-init / install-config feature

v0.0.3
- Added tools to create init script and configuration files in /etc
- Added ping feature
- More robust/fault tolerant
- Handles pika bug where AttributeError might be raised if connection is unexpectedly closed

v0.0.2
- Project is now a proper python project
- Included uptime
- IP Addresses and uptime are sent at longer intervals
- Only sends memory as a percentage of usage
- Install procedures for an init script and configuration

v0.0.1

Initial release!
 
