#!/usr/bin/env python
import os
import sys
import subprocess
import glob

mydir = os.path.dirname(os.path.realpath(__file__))
projectdir = os.path.realpath(mydir + "/../")

def dist_metadata():

    f = glob.glob('dist/*.tar.gz')[0].split('dist/')[1]
    
    fparts = f.split('-')
    version = fparts[-1:][0].split('.tar.gz')[0]

    name = '-'.join(fparts[:-1])

    return (name, version)


def out(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

def outnl(msg):
    out(msg + "\n")


def execute_cmd(args):
    outnl(str(args))
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while p.poll() is None:
        for line in iter(p.stdout.readline, ''):
            out(line)

    if p.returncode != 0:
        raise RuntimeError("Failed to execute cmd: %s" % p.returncode)
        raise "Failed to execute cmd"


buildnumber = 1
if len(sys.argv) > 1:
    buildnumber = sys.argv[1]

os.chdir(projectdir)

execute_cmd(['pip','install','stdeb'])
execute_cmd(['python', 'setup.py', 'sdist'])
execute_cmd(['python', 'setup.py', '--command-packages=stdeb.command','sdist_dsc','--debian-version=%s' % buildnumber])

name, version = dist_metadata()

outnl("Package: %s" % name)
outnl("Version: %s" % version)

execute_cmd(['cp', 'debian2/psistats.init', 'deb_dist/%s-%s/debian/psistats.init' % (name, version)])
execute_cmd(['cp', 'debian2/psistats.upstart', 'deb_dist/%s-%s/debian/psistats.upstart' % (name, version)])
execute_cmd(['cp', 'debian2/psistats.postinst', 'deb_dist/%s-%s/debian/psistats.postinst' % (name, version)])

os.chdir('deb_dist/%s-%s' % (name, version))
#execute_cmd(['dpkg-buildpackage', '-us', '-uc'])

#os.chdir(projectdir)
#execute_cmd(['mv', 'deb_dist/%s_%s-%s_all.deb' % (name, version, buildnumber),'dist/'])
