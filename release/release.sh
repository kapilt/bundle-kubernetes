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


    REPOPATH=`pwd`"git/${CHARM}"
    if [ -d  $REPOPATH ]
    then
        echo "git/${CHARM}: $REPO exists"
        cd $REPOPATH
        git pull --rebase
    else
        pushd . && cd git
        git clone $REPO $CHARM
    fi
    popd


    CHARMPATH=`pwd`"git/${CHARM}"
    if [ -d $CHARMPATH ]
    then
        pushd . && cd $CHARMPATH
        echo "lp/${CHARM}: $REPO exists"
    else
        pushd . && cd lp
        bzr branch $TARGET $CHARM
    fi
    popd


done
