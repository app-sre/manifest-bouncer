#!/bin/bash

WORKDIR="$PWD/saas-repos"

rm -rf "$WORKDIR"; mkdir -p "$WORKDIR"

cd "$WORKDIR"

cat - | xargs -P0 -n1 git clone -q

for saasrepo in `find "$WORKDIR" -mindepth 1 -maxdepth 1 -type d`; do
    cd "$saasrepo"

    for context in $(saasherder config get-contexts); do
        saasherder --context $context --environment production pull
        saasherder --context $context --environment production template --local tag
    done
done

