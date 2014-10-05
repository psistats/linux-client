Psistats Linux Client
=====================

Version: 0.0.4-dev
------------------

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
}
```

Uptime is in seconds.

Uptime and IP Addresses are sent at a longer rate than cpu and memory however that rate is configurable.

CPU Temperature is enabled by default, but may not work on all systems.


Installation (From Source):
---------------------------

You can either checkout the source from here, or you can download the source from Psikon's repository.

- Snapshots: http://repo.psikon.org/psistats/clients/linux/snapshot
- Releases: http://repo.psikon.org/psistats/clients/linux/release

1. python setup.py install
2. edit psistats.conf to your liking
3. run psistats start


Installation (Ubuntu 12.04 and higher):
---------------------------------------

Psikon now has a Debian/Ubuntu repository to make installation easier. You can either choose stable or snapshot releases. For stable releases run the following commands:

```
$ wget http://debrepo.psikon.org/conf/debrepo.gpg.key
$ sudo apt-key add debrepo.gpg.key
$ sudo add-apt-repository 'deb http://debrepo.psikon.org/beta [distro] main'
$ sudo apt-get update
$ audo apt-get install psistats-client
```

Replace [distro] with your Ubuntu distribution name:

* 12.04 - oneiric
* 12.10 - precise
* 13.04 - raring
* 13.10 - saucy
* 14.04 - trusty


Changelog
---------
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
 
