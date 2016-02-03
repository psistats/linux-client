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

WARNING: The debian repo is currently inactive. A PPA will be available soon.

Psikon now has a Debian/Ubuntu repository to make installation easier. You can either choose stable or snapshot releases. For stable releases run the following commands:

```
$ wget http://debrepo.psikon.org/conf/debrepo.gpg.key
$ sudo apt-key add debrepo.gpg.key
$ sudo add-apt-repository 'deb http://debrepo.psikon.org [distro] main'
$ sudo apt-get update
$ audo apt-get install psistats-client
```

Replace [distro] with your distrubtion name:

* Ubuntu 12.04 - oneiric
* Ubuntu 12.10 - precise
* Ubuntu 13.04 - raring
* Ubuntu 13.10 - saucy
* Ubuntu 14.04 - trusty
* Raspbian - wheezy
* Debian 7.0 - wheezy

NOTE: For Ubunbut v13.10 and lower, you must upgrade the pika python library:

```
$ sudo pip install --upgrade pika
```

For snapshot builds, use http://debrepo.psikon.org/beta

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
primary_timer=1
secondary_timer=30
retry_timer=5
pidfile=/var/run/psistats.pid
pidfile_timeout=5
stdin_path=/dev/null
stdout_path=/dev/null
stderr_path=/dev/null
```

* **primary_timer:** The main timer, in seconds.
* **secondary_timer:** The secondary timer to broadcast IP and Uptime, in seconds
* **retry_timer:** Timer, in seconds, to reconnect to RabbitMQ when the connection is lost
* **pidfile:** Location of pidfile
* **pidfile_timeout:** Pidfile lock timeout
* **stdin_path:** Where to send stdin
* **stdout_path:** Where to send stdout
* **stderr_path:** Where to send stdrr

###Misc Settings

```
[cpu_temp]
enabled=1

[cpu]
enabled=1

[mem]
enabled=1

[ipaddr]
enabled=1

[uptime]
enabled=1

[hostname]
enabled=1
```
* **enabled:** Turn on or off various parts of the information that's sent out

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
 
