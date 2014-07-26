#!/bin/sh
rm -rf build
rm -rf dist
rm -rf psistats.egg-info
update-rc.d -f psistats remove
rm /etc/psistats.conf
rm /etc/init.d/psistats
pip uninstall -y psistats
python setup.py install
psistats install-init
psistats install-config

