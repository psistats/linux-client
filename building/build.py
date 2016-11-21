#!/usr/bin/env python
import os
import sys
import subprocess
import glob
import argparse
import time

argparser = argparse.ArgumentParser(description='Psistats Builder')
arggroup_meta = argparser.add_argument_group('Metadata')
arggroup_meta.add_argument('--build-number', help='Build Number')
arggroup_dirs = argparser.add_argument_group('Directories')
arggroup_dirs.add_argument('--project-dir', help='Project Directory')
arggroup_sec  = argparser.add_argument_group('Security')
arggroup_sec.add_argument('--gpg-key', help='GPG Key used for signing')

args = vars(argparser.parse_args())

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
        for line in iter(p.stderr.readline, ''):
            out(line)
        raise RuntimeError("Failed to execute cmd: %s" % p.returncode)
        raise "Failed to execute cmd"

if args['project_dir'] != None:
    projectdir = args['project_dir']
else:
    mydir = os.path.dirname(os.path.realpath(__file__))
    projectdir = os.path.realpath(mydir + "/../")

gpgkey = args['gpg_key']

outnl('Project Directory: %s' % projectdir)


buildnumber = 1
if (args['build_number'] != None):
    buildnumber = int(args['build_number'])

outnl('----> BUILD INFO')
outnl('Project Directory: %s' % projectdir)
outnl('Build Number     : %s' % buildnumber)
outnl('----> BUILD OUTPUT')

os.chdir(projectdir)

# execute_cmd(['pip','install','stdeb'])
execute_cmd(['python', 'setup.py', 'sdist'])
# execute_cmd(['python', 'setup.py', '--command-packages=stdeb.command','sdist_dsc','--debian-version=%s' % buildnumber, '--suite=psikon-unstable'])

name, version = dist_metadata()
debversion = version + "-%s" % buildnumber

outnl("Package: %s" % name)
outnl("Version: %s" % version)
outnl("Debian Version: %s" % debversion)

changelog = """%s (%s) unstable; urgency=medium

  * Changelog

 -- Alex Dowgailenko <adow@psikon.com>  %s

"""

debdir = 'deb_dist/%s-%s/debian' % (name, version)
tarball = 'dist/%s-%s.tar.gz' % (name, version)

changelog = changelog % (name, debversion, time.strftime('%a, %d %b %Y %H:%M:%S +0500'))


execute_cmd(['mkdir', '-p', debdir])
execute_cmd(['cp', tarball, debdir + '/../../%s_%s.orig.tar.gz' % (name, version)])
execute_cmd(['tar', '-xzvf', 'deb_dist/%s_%s.orig.tar.gz' % (name, version), '-C', debdir + '/../..'])
execute_cmd(['cp', 'debian3/compat', debdir])
execute_cmd(['cp', 'debian3/control', debdir])
execute_cmd(['cp', '-r', 'debian3/source', debdir])
execute_cmd(['cp', 'debian3/copyright', debdir])
execute_cmd(['cp', 'debian3/rules', debdir])
execute_cmd(['cp', 'debian3/psistats.init', debdir])
execute_cmd(['cp', 'debian3/conffiles', debdir])
# execute_cmd(['cp', 'debian3/psistats.upstart', debdir])
execute_cmd(['cp', 'debian3/psistats.postinst', debdir])
with open(debdir + '/changelog', 'w') as f:
    f.write(changelog)

# sys.exit()
# with open('dist/%s-%s/debian/changelog
#execute_cmd(['cp', 'debian2/psistats.init', 'deb_dist/%s-%s/debian/psistats.init' % (name, version)])
#execute_cmd(['cp', 'debian2/psistats.upstart', 'deb_dist/%s-%s/debian/psistats.upstart' % (name, version)])
#execute_cmd(['cp', 'debian2/psistats.postinst', 'deb_dist/%s-%s/debian/psistats.postinst' % (name, version)])
#execute_cmd(['cp', 'debian2/conffiles', 'deb_dist/%s-%s/debian/conffiles' % (name, version)])
#execute_cmd(['cp', 'debian2/control', 'deb_dist/%s-%s/debian/control' % (name, version)])
#execute_cmd(['cp', 'debian2/rules', 'deb_dist/%s-%s/debian/rules' % (name, version)])

#if gpgkey != None:
#    execute_cmd(['debsign', '-k', gpgkey, 'deb_dist/%s_%s_source.changes' % (name, debversion)])

"""
newcontent = []
with open('deb_dist/%s-%s/debian/control' % (name, version)) as f:
    
    found = False

    for line in f.readlines():
        if line == "\n" and found == False:
            newcontent.append('Version: %s\n' % debversion)
            found = True
        else:
            newcontent.append(line)
with open('deb_dist/%s-%s/debian/control' % (name, version), 'w') as f:
    f.write(''.join(newcontent))
"""

os.chdir('deb_dist/%s-%s' % (name, version))

# execute_cmd(['dpkg-buildpackage', '-us', '-uc'])

execute_cmd(['debuild','-us','-uc'])

os.chdir(projectdir)
if gpgkey != None:
    execute_cmd(['debsign', '-k', gpgkey, 'deb_dist/%s_%s_amd64.changes' % (name, debversion)])
#    execute_cmd(['debsigs', '--sign=origin', '-k', gpgkey, 'deb_dist/%s_%s_all.deb' % (name, debversion)])

execute_cmd(['cp', 'deb_dist/%s_%s-%s_all.deb' % (name, version, buildnumber), 'dist/'])
