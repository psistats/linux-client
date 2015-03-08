#!/bin/bash
PATH_SELF=$( cd "$( dirname "$0" )" && pwd)
source $PATH_SELF/variables.sh

cd $PROJECT_DIR

cmd () {
    echo "[RUN] $1"
    eval $1
    if [ $? -ne 0 ]; then
        exit $?
    fi
}

VERSION=$( python setup.py --version )
ARTIFACT_ID=$( python setup.py --name )

NEW_VERSION=${VERSION/\-dev/}

if [ $1="new_minor" ]; then
    IFS="." read -ra VERS <<< $NEW_VERSION
    (( VERS[1]++ ))
    VERS[2]=0
    for i in "${VERS[@]}"; do
        echo $i
    done
    NEW_VERSION=$( IFS="."; echo "${VERS[*]}" )
    echo $NEW_DEV_VERSION
elif [ $1="new_major"]; then
    IFS="." read -ra VERS <<< $NEW_VERSION
    (( VERS[0]++ ))
    VERS[1]=0
    VERS[2]=0
    NEW_VERSION=$( IFS="."; echo "${VERS[*]}" )
else
    IFS="." read -ra VERS <<< $NEW_VERSION
    (( VERS[2]++ ))
    NEW_VERSION=$( IFS="."; echo "${VERS[*]}" )
fi

echo "Building $NEW_VERSION"

cmd "git checkout -b \"v$NEW_VERSION\""

cmd "python building/new-version.py $NEW_VERSION"

cmd "git commit sonar-project.properties setup.py VERSION -m \"Changing version from $VERSION to $NEW_VERSION\""

cmd "building/build.sh"

cmd "git checkout master"

IFS="." read -ra VERS <<< $NEW_VERSION
(( VERS[2]++ ))
NEW_DEV_VERSION=$( IFS="."; echo "${VERS[*]}" )

NEW_DEV_VERSION=$NEW_DEV_VERSION-dev

echo "Creating new dev version: $NEW_DEV_VERSION"

cmd "python building/new-version.py $NEW_DEV_VERSION"

cmd "git commit sonar-project.properties setup.py VERSION -m \"Changing version from $VERSION to $NEW_DEV_VERSION\""
cmd "git push"
cmd "git checkout v$NEW_VERSION"
cmd "git push -u origin v$NEW_VERSION"
