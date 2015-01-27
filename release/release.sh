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

    if [ -d "git/${CHARM}" ]
    then
        echo "git/${CHARM}: $REPO exists"
    else
        pushd . && cd git
        git clone $REPO $CHARM
        popd
    fi

    if [ -d "lp/${CHARM}" ]
    then
        echo "lp/${CHARM}: $REPO exists"
    else
        pushd . && cd lp
        bzr branch $TARGET $CHARM
        popd
    fi

done
