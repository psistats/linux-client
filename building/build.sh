#!/bin/bash

PATH_SELF=$( cd "$( dirname "$0" )" && pwd )
PROJECT_DIR=$PATH_SELF/..

cmd () {
    echo "[RUN] $1"
    eval $1
    if [ $? -ne 0 ]; then
        exit $?
    fi
}

cmd "cd $PROJECT_DIR"

VERSION=$( python setup.py --version )
ARTIFACT_ID=$( python setup.py --name )


cmd "rm -rfv building/venv"
cmd "virtualenv building/venv"
cmd "source building/venv/bin/activate"
cmd "pip install stdeb"
cmd "python setup.py clean --all"
cmd "python setup.py test --addopt \"--cov=psistats --cov-report=html --cov-report=xml --cov-report=annotate\""
cmd "python setup.py install"
cmd "python setup.py sdist"
cmd "python setup.py --command-packages=stdeb.command sdist_dsc"
cmd "cd deb_dist/$ARTIFACT_ID-$VERSION"
cmd "cp ../../debian/* ./debian/"
cmd "dpkg-buildpackage -rfakeroot -uc -us"
#cmd "python setup.py --command-packages=stdeb.command bdist_deb"


#KEY=98A870F9
#DEBDIST_DIR=$SRC_DIR/deb_dist
#DEBIAN_DIR=$DEBDIST_DIR/$ARTIFACT_ID-$VERSION/debian
#DEB_FILE=${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}_all.deb
#
#cd $DEBDIST_DIR
#cmd "debsign -S --re-sign -k$KEY ${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}_source.changes"
#cmd "debsign -S --re-sign -k$KEY ${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}.dsc"
#
echo "---------------------"
echo "Build finished!"
