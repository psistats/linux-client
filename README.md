Psistats Linux Client
=====================

Version: 0.0.4-SNAPSHOT
--------------

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


Installation
------------

1) python setup.py install
2) sudo psistats install-config
3) sudo psistats install-init
4) Edit /etc/psistats.conf to your liking.
5) sudo psistats start


Uninstallation
--------------

1) pip uninstall psistats
2) update-rc.d -f psistats remove (if necessary)
3) rm /etc/init.d/psistats
4) rm /etc/psistats.conf
5) rm /usr/local/bin/psistats


Changelog
---------
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
 
