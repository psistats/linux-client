#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  TARGET="$(readlink "$SOURCE")"
  if [[ $SOURCE == /* ]]; then
    echo "SOURCE '$SOURCE' is an absolute symlink to '$TARGET'"
    SOURCE="$TARGET"
  else
    DIR="$( dirname "$SOURCE" )"
    echo "SOURCE '$SOURCE' is a relative symlink to '$TARGET' (relative to '$DIR')"
    SOURCE="$DIR/$TARGET" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  fi
done
echo "SOURCE is '$SOURCE'"
RDIR="$( dirname "$SOURCE" )"
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
if [ "$DIR" != "$RDIR" ]; then
  echo "DIR '$RDIR' resolves to '$DIR'"
fi
echo "DIR is '$DIR'"


VERSION=$(cat VERSION)
ARTIFACT_ID=psistats
CONFIG=$DIR/build-configs/debian/stdeb.cfg

echo "CONFIG is '$CONFIG'"

python setup.py --command-packages=stdeb.command sdist_dsc --extra-cfg-file=$CONFIG
cd deb_dist/$ARTIFACT_ID-$VERSION
dpkg-buildpackage -rfakeroot -uc -us

