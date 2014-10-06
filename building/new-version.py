import sys
import os

if "NEW_VERSION" not in os.environ:
    print "[ERROR] Missing NEW_VERSION environment variable"
    sys.exit(1)

NEW_VERSION = os.environ["NEW_VERSION"]

PROJECT_DIR = os.path.realpath(os.path.dirname(__file__) + "/../")

with open(PROJECT_DIR + "/VERSION") as f:
    VERSION = f.read().strip()

with open(PROJECT_DIR + "/VERSION", "w") as f:
    f.write(NEW_VERSION)

with open(PROJECT_DIR + "/setup.py") as f:
    setup_file = f.read()

with open(PROJECT_DIR + "/setup.py", "w") as f:
    f.write(setup_file.replace(VERSION, NEW_VERSION))

with open(PROJECT_DIR + "/sonar-project.properties") as f:
    sonarprops = f.read()

with open(PROJECT_DIR + "/sonar-project.properties", "w") as f:
    f.write(sonarprops.replace(VERSION, NEW_VERSION))
