#!/usr/bin/env python
import os
import sys
import shutil
import glob

mydir = os.path.dirname(os.path.realpath(__file__))
projectdir = os.path.realpath(mydir + "/../")

dirs = ['dist','deb_dist','build','.tox','.eggs','covenv','.cache','psistats.egg-info']
files = ['psistats-0.2.0develop.tar.gz']

def out(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()

for d in dirs:
    try:
        targetdir = projectdir + "/" + d
        shutil.rmtree(targetdir)
        out(targetdir)
    except OSError:
        pass

for f in files:
    try:
        targetfile = projectdir + "/" + f
        os.remove(targetfile)
        out(targetfile)
    except OSError:
        pass

for f in glob.glob('./*/*.pyc'):
    try:
        out(f)
        os.remove(f)
    except OSError:
        pass

