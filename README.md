Psistats Linux Client
=====================

Python linux client that sends some computer statistics to a RabbitMQ
server.

Format
------
```javascript
{
    "hostname": "my-computer",
    "uptime": 130583.1,
    "cpu": 24.1,
    "mem": 34.1,
    "ipaddr": ['192.168.1.101','192.168.1.102']
    "cpu_temp": 72.4
}
```

Uptime is in seconds.

Uptime and IP Addresses are sent at a longer rate than cpu and memory however that rate is configurable.

CPU Temperature is enabled by default, but may not work on all systems. It is reported in degrees celsius.


Installation (From Source):
---------------------------

1. python setup.py install
2. edit psistats.conf to your liking
3. run psistats start


Installation (Ubuntu 12.04+ / RaspberryPi / Debian Wheezy):
---------------------------------------

WARNING: Debian packages are currently unavailable.

Currently you can install from source, then link /usr/bin/psistats to /etc/init.d/psistats to have psistats start on boot.


Configuration
-------------

###Queue Settings:

```
[queue]
prefix=psistats
exclusive=True
durable=False
autodelete=Yes
ttl=10000
```

* **prefix:** The queue name will be [prefix].[hostname].
* **exclusive:** Whether or not the queue can be used by other clients.
* **durable:** Whether or not the queue will be recreated automatically upon server restart
* **autodelete:** Whether or not the queue will be removed when there are no more clients using it
* **ttl:** How long, in milliseconds, will messages remain in the queue

###Exchange Settings:

```
[exchange]
name=psistats
type=topic
durable=False
autodelete=False
```

* **name:** The exchange name.
* **type:** What kind of exchange it should be.
* **durable:** Whether or not the exchange will be recreated automatically upon server restart
* **autodelete:** Whether or not the exchange will be removed when there are no more clients using it

###Server Settings:

```
[server]
url=amqp://guest:guest@localhost:5672/
```

* **url:** URL (using amqp for the scheme) for the RabbitMQ server

###Application Settings

```
[app]
retry_timer=5
pidfile=/var/run/psistats.pid
pidfile_timeout=5
stdin_path=/dev/null
stdout_path=/dev/null
stderr_path=/dev/null
```

* **retry_timer:** Timer, in seconds, to reconnect to RabbitMQ when the connection is lost
* **pidfile:** Location of pidfile
* **pidfile_timeout:** Pidfile lock timeout
* **stdin_path:** Where to send stdin
* **stdout_path:** Where to send stdout
* **stderr_path:** Where to send stdrr

###Reporters

Various reporters are available from psistats, but some have additional dependencies that you will have to install separately.

#### Sensors

The `hddtemp` reporter reports the temperatures of all your drives (if supported) and requires https://wiki.archlinux.org/index.php/Hddtemp to be installed as well as have the daemon running.

The `sensors` reporter can report any value from any available sensor and requires libsensors to be installed.

Debian users can just do this:

```
sudo apt-get install hddtemp libsensors4
```

#### Other Reporters

For more information, refer to the psistats.conf file.

###Logging Configuration

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
- New multithreaded architecture
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
 
