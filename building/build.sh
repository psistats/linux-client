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

cd $PROJECT_DIR

if [ ! -f $PYENV_DIR/bin/activate ]; then
    cmd "rm -rfv $PYENV_DIR"
    cmd "virtualenv $PYENV_DIR"
fi
mkdir -p $COVERAGE_HTML_DIR
mkdir -p $COVERAGE_XML_DIR

VERSION=$( python setup.py --version )
ARTIFACT_ID=$( python setup.py --name )

cat << EOT > $TARGET_DIR/env.properties
VERSION=$VERSION
ARTIFACT_ID=$ARTIFACT_ID
BUILD_NUMBER=$BUILD_NUMBER
EOT
 

cmd "source $PYENV_DIR/bin/activate"
cmd "pip install coverage mock stdeb nose"
cmd "python setup.py install"
cmd "nosetests --verbose --with-coverage --cover-html --cover-html-dir=$COVERAGE_HTML_DIR --cover-package=psistats --cover-xml --cover-xml-file=$COVERAGE_XML_DIR/coverage.xml --with-xunit --xunit-file=$COVERAGE_DIR/xunit.xml -d"
cmd "python setup.py sdist --dist-dir=$DIST_DIR"

cd $DIST_DIR
cmd "tar -xzvf ${ARTIFACT_ID}-${VERSION}.tar.gz"

SRC_DIR=$DIST_DIR/${ARTIFACT_ID}-${VERSION}
cd $SRC_DIR
cmd "python setup.py --command-packages=stdeb.command sdist_dsc --extra-cfg-file=$DEBIAN_CFG_DIR/configs/debian.cfg --debian-version=$BUILD_NUMBER --package=$ARTIFACT_ID"

DEBDIST_DIR=$SRC_DIR/deb_dist
DEBIAN_DIR=$DEBDIST_DIR/$ARTIFACT_ID-$VERSION/debian
DEB_FILE=${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}_all.deb
cmd "sed -i -e 's/python-all (>= 2.6.6-3), //g' $DEBDIST_DIR/${ARTIFACT_ID}_${VERSION}-${BUILD_NUMBER}.dsc"

cmd "cp $DEBIAN_CFG_DIR/postinst $DEBIAN_DIR/postinst"
cmd "cp $DEBIAN_CFG_DIR/postrm $DEBIAN_DIR/postrm"
cmd "cp -r $DEBIAN_CFG_DIR/conffiles $DEBIAN_DIR/conffiles"

cd $DEBIAN_DIR/../
cmd "dpkg-buildpackage -rfakeroot -uc -us -d"
cmd "mkdir -p $TARGET_DIR/temp"
cmd "cp $DEBDIST_DIR/$DEB_FILE $TARGET_DIR/temp"
cmd "dpkg-deb -x $TARGET_DIR/temp/$DEB_FILE $TARGET_DIR/temp/extracted"
cmd "dpkg-deb -e $TARGET_DIR/temp/$DEB_FILE $TARGET_DIR/temp/extracted/DEBIAN"
cmd "sed -i -e 's/python:any (>= 2.7.1-8ubuntu2), //g' $TARGET_DIR/temp/extracted/DEBIAN/control"
cmd "dpkg-deb -b $TARGET_DIR/temp/extracted $DIST_DIR/$DEB_FILE"

echo "---------------------"
echo "Build finished!"
