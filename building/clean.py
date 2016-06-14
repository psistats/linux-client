#!/usr/bin/env python
import os
import sys
import shutil
import glob
import fnmatch

mydir = os.path.dirname(os.path.realpath(__file__))
projectdir = os.path.realpath(mydir + "/../")

dirs = ['dist','deb_dist','build','.tox','.eggs','covenv','.cache','psistats.egg-info','env-build','testenv']
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

for root, dirnames, filenames in os.walk(projectdir):
    if root.endswith("__pycache__"):
        out(root)
        shutil.rmtree(root)
    else:
        for fn in filenames:
            if fn.endswith('.pyc'):
                out(f)
                os.remove(f)

