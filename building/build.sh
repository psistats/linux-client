#!/bin/bash

PATH_SELF=$( cd "$( dirname "$0" )" && pwd )
source $PATH_SELF/variables.sh

cmd () {
    echo "[RUN] $1"
    eval $1
    if [ $? -ne 0 ]; then
        exit $?
    fi
}

echo Project Root: $PROJECT_DIR
cd $PROJECT_DIR

if [ ! -f $PYENV_DIR/bin/activate ]; then
    cmd "rm -rfv $PYENV_DIR"
    cmd "virtualenv $PYENV_DIR"
fi

VERSION=$( python setup.py --version )
ARTIFACT_ID=$( python setup.py --name )

cat << EOT > $TARGET_DIR/env.properties
VERSION=$VERSION
ARTIFACT_ID=$ARTIFACT_ID
BUILD_NUMBER=$BUILD_NUMBER
EOT
 

cmd "source $PYENV_DIR/bin/activate"
cmd "pip install stdeb"
cmd "python setup.py sdist --dist-dir=$DIST_DIR"

cd $DIST_DIR
cmd "tar -xzvf ${ARTIFACT_ID}-${VERSION}.tar.gz"

SRC_DIR=$DIST_DIR/${ARTIFACT_ID}-${VERSION}
cd $SRC_DIR
cmd "python setup.py --command-packages=stdeb.command sdist_dsc --debian-version=$BUILD_NUMBER --package=$ARTIFACT_ID"

KEY=98A870F9
DEBDIST_DIR=$SRC_DIR/deb_dist
DEBIAN_DIR=$DEBDIST_DIR/$ARTIFACT_ID-$VERSION/debian
DEB_FILE=${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}_all.deb

cd $DEBDIST_DIR
cmd "debsign -S --re-sign -k$KEY ${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}_source.changes"
cmd "debsign -S --re-sign -k$KEY ${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}.dsc"

echo "---------------------"
echo "Build finished!"
