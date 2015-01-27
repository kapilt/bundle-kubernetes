#!/bin/bash

# Download the charms from git and bzr that are in the .config.json file.
# Create a new tag which should be in the format vN.N.N
# Copy the github code over the bzr code.
# Push the new bzr code to launchpad.

# The first argument should be the tag and it should be in the format 
# vN.N.N to match the kubernetes version that the charms support by default.

set -ex

GR=$(jq -r .repos[].git ./.config.json)
LP=$(jq -r .repos[].lp ./.config.json)

readarray -t gitrepos <<<"$GR"
readarray -t bzrrepos <<<"$LP"

mkdir -p git
mkdir -p lp

for i in "${!gitrepos[@]}"; do
    REPO="${gitrepos[$i]}"
    TARGET="${bzrrepos[$i]}"
    CHARM=`basename $(dirname $TARGET)`
    echo $i $CHARM $REPO $TARGET

    REPOPATH=`pwd`"/git/${CHARM}"
    if [ -d  $REPOPATH ]
    then
        echo "git/${CHARM}: $REPO exists"
        pushd . && cd $REPOPATH
        git pull --rebase
    else
        pushd . && cd git
        git clone $REPO $CHARM
    fi
    popd


    CHARMPATH=`pwd`"/lp/${CHARM}"
    if [ -d $CHARMPATH ]
    then
        pushd . && cd $CHARMPATH
        echo "lp/${CHARM}: $REPO exists"
    else
        pushd . && cd lp
        bzr branch $TARGET $CHARM
    fi
    popd

    pushd .
    cd $REPOPATH
    git tag $1 && git push --tags
    git-vendor sync -t $1 -d $CHARMPATH
    cd $CHARMPATH
    bzr add && bzr tag $1 && bzr commit -m "Release ${1}"
    bzr push $TARGET
    popd

done
