#!/bin/bash
#WORKSPACE=/home/v0idnull/tmp/psistatsrd
GIT_DIR=$WORKSPACE/git
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
