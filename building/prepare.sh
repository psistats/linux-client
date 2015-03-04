#!/bin/bash
PATH_SELF=$( cd "$( dirname "$0" )" && pwd )
source $PATH_SELF/variables.sh

rm -rfv $PROJECT_DIR/build
rm -rfv $PROJECT_DIR/psistats_client.egg-info
rm -rfv $PROJECT_DIR/dist
rm -rfv $BUILD_DIR
rm -rfv $TARGET_DIR

