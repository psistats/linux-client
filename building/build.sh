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

cmd "source $PYENV_DIR/bin/activate"
cmd "pip install coverage mock stdeb"
cmd "python setup.py install"
cmd "python setup.py test"
cmd "python setup.py coverage --branch --erase --html-dir=$COVERAGE_HTML_DIR --xml-dir=$COVERAGE_XML_DIR --annotations-dir=$COVERAGE_ANNOTATIONS_DIR"
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
cmd "mkdir $TARGET_DIR/temp"
cmd "cp $DEBDIST_DIR/$DEB_FILE $TARGET_DIR/temp"
cmd "dpkg-deb -x $TARGET_DIR/temp/$DEB_FILE $TARGET_DIR/temp/extracted"
cmd "dpkg-deb -e $TARGET_DIR/temp/$DEB_FILE $TARGET_DIR/temp/extracted/DEBIAN"
cmd "sed -i -e 's/python:any (>= 2.7.1-8ubuntu2), //g' $TARGET_DIR/temp/extracted/DEBIAN/control"
cmd "dpkg-deb -b $TARGET_DIR/temp/extracted $DIST_DIR/$DEB_FILE"
