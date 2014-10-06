import sys
import os

PROJECT_DIR = os.path.realpath(os.path.dirname(__file__) + "/../")

with open("VERSION") as f:
    VERSION = f.read()

VERSION = VERSION.replace("-dev", "")

with open("VERSION", "w") as f:
    f.write(VERSION)

with open("setup.py") as f:
    setup_file = f.read()

with open("setup.py", "w") as f:
    f.write(setup_file.replace(VERSION + "-dev", VERSION))

with open("sonar-project.properties") as f:
    sonarprops = f.read()

with open("sonar-project.properties", "w") as f:
    f.write(sonarprops.replace(VERSION + "-dev", VERSION))
