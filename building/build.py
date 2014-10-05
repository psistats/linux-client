import logging
import sys
import subprocess
import os
import shutil

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)

root.addHandler(ch)

if 'ARTIFACT_ID' not in os.environ:
    root.fatal('No ARTIFACT_ID environment variable found.')
    sys.exit(1)

if 'VERSION' not in os.environ:
    root.fatal('No VERSION environment variable found.')
    sys.exit(1)
    
if 'BUILD_NUMBER' not in os.environ:
    root.fatal('No BUILD_NUMBER environment variable found.')
    sys.exit(1)

ARTIFACT_ID = os.environ['ARTIFACT_ID']
VERSION = os.environ['VERSION']
BUILD_NUMBER = os.environ['BUILD_NUMBER']

PROJECT_DIR = os.path.realpath(os.path.dirname(__file__) + "/../")
DIST_DIR = PROJECT_DIR + "/dist"
SRC_DIR = "%s/%s-%s" % (DIST_DIR, ARTIFACT_ID, VERSION)
BUILD_DIR = PROJECT_DIR + "/build"
DEBIAN_CFG_DIR = PROJECT_DIR + "/building/debian"
DEBIAN_CONFIG = DEBIAN_CFG_DIR + "/config/debian.cfg"
POSTINST_SCRIPT = DEBIAN_CFG_DIR + "/postinst"
POSTRM_SCRIPT = DEBIAN_CFG_DIR + "/postrm"
CONFFILES = DEBIAN_CFG_DIR + "/conffiles"
DEBDIST_DIR = "%s/%s-%s/deb_dist" % (DIST_DIR, ARTIFACT_ID, VERSION)
DEBIAN_DIR = "%s/%s-%s/debian" % (DEBDIST_DIR, ARTIFACT_ID, VERSION)
DEB_FILE = "%s/%s_%s-%s_all.deb" % (DEBDIST_DIR, ARTIFACT_ID, VERSION, BUILD_NUMBER)


root.info("Project directory: " + PROJECT_DIR)
root.info("Dist directory: " + DIST_DIR)


root.info("Cleaning up")

try:
    shutil.rmtree(DIST_DIR)
    shutil.rmtree(BUILD_DIR)
    shutil.rmtree(PROJECT_DIR + "/psistats-client.egg-info")
except OSError as e:
    if e.errno == 2:
        pass
    else:
        raise e

root.info("Building source")

def run_process(args):
    root.info("Executing " + " ".join(args))
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while p.poll() is None:
        root.info(p.stdout.readline().strip())

    if p.returncode != 0:
        for line in p.stderr.readlines():
            root.error(line)
        root.error("Failed! Error code %s" % p.returncode)
        return False
    return True


if run_process(('python', 'setup.py', 'sdist')) == False:
    root.fatal("Was not able to build source tarball")
    sys.exit(1)

os.chdir(DIST_DIR)


if run_process(('tar','-xzvf',"%s-%s.tar.gz" % (ARTIFACT_ID, VERSION))) == False:
    root.fatal("Was not unable to extract source tarball")
    sys.exit(1)

os.chdir(SRC_DIR)

sdist_cmd = (
    'python',
    'setup.py',
    '--command-packages=stdeb.command',
    'sdist_dsc',
    '--extra-cfg-file=' + DEBIAN_CONFIG,
    '--debian-version=' + BUILD_NUMBER,
    '--package=' + ARTIFACT_ID
)

if (run_process(sdist_cmd)) == False:
    root.fatal("Was not able to build debian source package")
    sys.exit(1)


root.info("Copying debian files to %s" % DEBIAN_DIR)
shutil.copy(POSTINST_SCRIPT, DEBIAN_DIR)
shutil.copy(POSTRM_SCRIPT, DEBIAN_DIR)
shutil.copy(CONFFILES, DEBIAN_DIR)

os.chdir(DEBIAN_DIR + "/../")

# cp -r python-$ARTIFACT_ID/etc python-$ARTIFACT_ID/share/psistats

if (run_process(('dpkg-buildpackage', '-rfakeroot', '-uc', '-us')) == False):
    root.fatal("Was not able to build debian binary package")
    sys.exit(1)

root.info("Copying %s to %s" % (DEB_FILE, DIST_DIR))
shutil.copy(DEB_FILE, DIST_DIR)

root.info("Cleaning up")
shutil.rmtree(SRC_DIR)

root.info("Success!")
