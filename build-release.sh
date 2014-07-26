#!/bin/bash
JENKINS_HOME="/psikon/.jenkins/"
INC_MAINT="true"
INC_MINOR="false"
INC_MAJOR="false"
WORKSPACE=$JENKINS_HOME/jobs/psistats-client-nix/workspace

VERSION=`cat $WORKSPACE/VERSION`

IFS="." read -ra VERPARTS <<< "$VERSION"

VER_MAINT=0
VER_MINOR=0
VER_MAJOR=0

if [ ${VERPARTS[2]} ]; then
    VER_MAINT=${VERPARTS[2]}
    echo "Maintenance version found"
fi

if [ ${VERPARTS[1]} ]; then
    VER_MINOR=${VERPARTS[1]}
    echo "Minor version found"
fi

if [ ${VERPARTS[0]} ]; then
    VER_MAJOR=${VERPARTS[0]}
    echo "Major version found"
fi

if [ "$INC_MAINT" == "true" ]; then
    VER_MAINT=`expr $VER_MAINT + 1`
fi

if [ "$INC_MINOR" == "true" ]; then
    VER_MINOR=`expr $VER_MINOR + 1`
fi

if [ "$INC_MAJOR" == "true" ]; then
    VER_MAJOR=`expr $VER_MAJOR + 1`
fi

NEW_VERSION=$VER_MAJOR.$VER_MINOR.$VER_MAINT

echo New version: $NEW_VERSION

svn copy https://dev.psikon.org/svn/psistats-client-nix/trunk https://dev.psikon.org/svn/psistats-client-nix/branches/$VERSION -m "Creating branch for version $VERSION"

sed -i "4s/.*/$NEW_VERSION/" $WORKSPACE/README.md
sed -i "4s/.*/sonar.projectVersion=$NEW_VERSION/" $WORKSPACE/sonar-project.properties

echo $NEW_VERSION > $WORKSPACE/VERSION

cd $WORKSPACE

svn commit VERSION README.md sonar-project.properties -m "Trunk switches to version $NEW_VERSION"

GIT_DIR=/psikon/tmp/psistatsrd-git
GIT_USERNAME=v0idnull
SVN_USERNAME=v0idnull
GIT_REPO=psistats-client-nix
SVN_URL=https://dev.psikon.org/svn/psistats-client-nix

if [ ! -d "$GIT_DIR" ]; then
    mkdir -p $GIT_DIR
    cd $GIT_DIR
    svn2git $SVN_URL --username v0idnull --verbose
    git remote add origin git@github.com:$GIT_USERNAME/$GIT_REPO.git
else
    cd $GIT_DIR
    svn2git --rebase
fi

cd $GIT_DIR

git commit -a
git commit -m "merge changes"
git pull origin master
git push origin master

git push origin $VERSION:$VERSION

