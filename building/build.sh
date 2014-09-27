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
export DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
if [ "$DIR" != "$RDIR" ]; then
  echo "DIR '$RDIR' resolves to '$DIR'"
fi
echo "DIR is '$DIR'"

export PROJECT_DIR=$( readlink -f "$DIR/../" )


export VERSION=$(cat VERSION)
export ARTIFACT_ID=psistats

echo "VERSION is '$VERSION'"
echo "ARTIFACT_ID is '$ARTIFACT_ID'"
echo "PROJECT_DIR id '$PROJECT_DIR'"

cd $PROJECT_DIR

$DIR/build-src.sh
RETCODE=$?

if [[ $RETCODE != 0 ]]; then
    echo "[ERROR] build-src.sh script failed"
    exit 1
fi

$DIR/build-debian.sh
if [[ $RETCODE != 0 ]]; then
    echo "[ERROR] build-debian.sh script failed"
    exit 1
fi


