#!/bin/bash
# Copy the charms from git and bzr that are in the .config.json file.

set -ex

LPBASE=$(jq -r .lpbase ./.config.json)

GR=$(jq -r .gitrepos[].git ./.config.json)
CN=$(jq -r .gitrepos[].lp ./.config.json)

readarray -t gitrepos <<<"$GR"
readarray -t charm_names <<<"$CN"

mkdir -p git
mkdir -p lp

for i in "${!gitrepos[@]}"; do
    REPO="${gitrepos[$i]}"
    CHARM="${charm_names[$i]}"
    TARGET="${LPBASE}/${CHARM}/trunk"
    echo $i $REPO $CHARM


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
    git-vendor sync -t $1 -d $CHARMPATH
    cd $CHARMPATH
    bzr add && bzr tag $1 && bzr commit -m "Release ${1}"
    bzr push $LPBASE/$CHARM/trunk
    popd

done
