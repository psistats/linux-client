#!/bin/bash
#########
# Build script for Psistats linux client
#
# Designed to work within a jenkins environment
#########

if [[ -z "$WORKSPACE" ]]; then
    WORKSPACE=.
fi

PYENV=$WORKSPACE/.pyenv
REPORTS=$WORKSPACE/.reports

# clean up first
rm -rfv $REPORTS
rm -rfv $PYENV
rm -rfv $WORKSPACE/build
rm -rfv $WORKSPACE/dist
rm -rfv $WORKSPACE/psistats.egg-info

find . -name "*.pyc"-print0 | xargs -0 rm -vrf


mkdir -v $REPORTS

virtualenv --no-site-packages $PYENV
. $PYENV/bin/activate

python setup.py install

if [ $? -ne 0 ]; then
    echo "Unable to install psistats"
    exit $?
fi

pylint --output-format=parseable --reports=y $WORKSPACE/psistats/ | tee $REPORTS/pylint.out

if [ $? -ne 0 ]; then
    echo "Pylint failed to execute properly"
    exit $?
fi


VERSION=$(cat $WORKSPACE/VERSION)

DIST_NAME=psistats-$VERSION
DIST_DIR=$WORKSPACE/dist/psistats-$VERSION

mkdir -v $DIST_DIR
cp -rv $WORKSPACE/bin $DIST_DIR
cp -rv $WORKSPACE/psistats $DIST_DIR
cp -v $WORKSPACE/README.md $DIST_DIR
cp -v $WORKSPACE/LICENSE $DIST_DIR
cp -v $WORKSPACE/INSTALL $DIST_DIR
cp -v $WORKSPACE/VERSION $DIST_DIR
cp -v $WORKSPACE/setup.py $DIST_DIR
cp -v $WORKSPACE/psistats.conf $DIST_DIR
cp -v $WORKSPACE/MANIFEST.in $DIST_DIR

cd $WORKSPACE/dist
tar -cvzf $DIST_NAME.tar.gz $DIST_NAME
cd $WORKSPACE

exit 0
