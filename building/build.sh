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

if [ -z "${BUILD_NUMBER}" ];
then 
  BUILD_NUMBER=1
fi

DEBDIST_DIR=$PROJECT_DIR/deb_dist
DEBSRC_DIR=${DEBDIST_DIR}/${ARTIFACT_ID}-${VERSION}
VENV_DIR=$PATH_SELF/venv

cmd "rm -rfv $VENV_DIR"
cmd "virtualenv $VENV_DIR"
cmd "source $VENV_DIR/bin/activate"
cmd "pip install stdeb"
cmd "python setup.py clean --all"
cmd "python setup.py install"
cmd "python setup.py sdist"
cmd "python setup.py --command-packages=stdeb.command sdist_dsc --debian-version=$BUILD_NUMBER"
cmd "cp $PROJECT_DIR/debian/* $DEBSRC_DIR/debian"
cmd "cd $DEBSRC_DIR"
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
