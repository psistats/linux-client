#!/bin/bash

echo "---- PREPARING DEBIAN PACKAGE ----"

DEBIAN_CFG_DIR=$DIR/debian
CONFIG=$DEBIAN_CFG_DIR/config/debian.cfg
POSTINST_SCRIPT=$DEBIAN_CFG_DIR/postinst
POSTRM_SCRIPT=$DEBIAN_CFG_DIR/postrm
CONFFILES=$DEBIAN_CFG_DIR/conffiles
SRC_DIR=$PROJECT_DIR/dist
DEBDIST_DIR=$SRC_DIR/$ARTIFACT_ID-$VERSION/deb_dist
DEBIAN_DIR=$DEBDIST_DIR/$ARTIFACT_ID-$VERSION/debian

echo "DEBIAN_CFG_DIR is $DEBIAN_CFG_DIR"
echo "DEBDIST_DIR is $DEBDIST_DIR"
echo "DEBIAN_DIR is $DEBIAN_DIR"

echo "CONFIG is '$CONFIG'"
echo "POSTINST_SCRIPT is $POSTINST_SCRIPT"
echo "POSTRM_SCRIPT is $POSTRM_SCRIPT"
echo "CONFFILES is $CONFFILES"

function execute_cmd {
    echo $1
    eval $1
    RETCODE=$?
    if [[ $RETCODE != 0 ]]; then
        echo $2
        exit $RETCODE
    fi
    
}


rm -rvf $DEBDIST_DIR

cd $SRC_DIR

execute_cmd "tar -xzvf $ARTIFACT_ID-$VERSION.tar.gz" \
    '[ERROR] Was unable to extract source tarball'

cd $ARTIFACT_ID-$VERSION

#execute_cmd "sed -i '12s/.*/data_files=[\\(\\\'\\\/etc\\\', [\\\'etc\\\/psistats.conf\\\']\\)]/' setup.py" \
#    '[ERROR] Was unable to fix setup.py'


CMD="python setup.py --command-packages=stdeb.command sdist_dsc --extra-cfg-file=$CONFIG --debian-version $BUILD_NUMBER --package $ARTIFACT_ID"

execute_cmd "$CMD" \
    '[ERROR] Was unable to call python setup.py to biuld debian source package!'

execute_cmd "cp -v $POSTINST_SCRIPT $DEBIAN_DIR" \
    "[ERROR] Was unable to copy $POSTINST_SCRIPT to $DEBIAN_DIR!"

execute_cmd "cp -v $POSTRM_SCRIPT $DEBIAN_DIR" \
    "[ERROR] Was unable to copy $POSTRM_SCRIPT to $DEBIAN_DIR!"

execute_cmd "cp -v $CONFFILES $DEBIAN_DIR" \
    "[ERROR] Was unable to copy $CONFFILES to $DEBIAN_DIR!"

cd $DEBIAN_DIR/../
# cp -r python-$ARTIFACT_ID/etc python-$ARTIFACT_ID/share/psistats 


execute_cmd "dpkg-buildpackage -rfakeroot -uc -us" \
    "[ERROR] Was unable to build debian package!"

cd $DEBDIST_DIR
