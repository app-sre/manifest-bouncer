#!/bin/bash

if [[ -n "$INSECURE_PULL" ]]; then
    INSECURE="--insecure"
else
    INSECURE=""
fi

WORKDIR="$PWD/saas-repos"

rm -rf "$WORKDIR"; mkdir -p "$WORKDIR"

cd "$WORKDIR"

cat - | xargs -P1 -n1 git clone -q

rc=0
for saasrepo in `find "$WORKDIR" -mindepth 1 -maxdepth 1 -type d`; do
    cd "$saasrepo"

    repo=$(git config --get remote.origin.url)
    if [[ $repo = "https://gitlab"* && -n "$GITLAB_TOKEN" ]]; then
        TOKEN="--token $GITLAB_TOKEN"
    else
        TOKEN=""
    fi

    for context in $(saasherder config get-contexts); do
        for service in $(saasherder --environment production get-services --context $context); do
            hash_len=$(saasherder --context $context --environment production get hash $service | wc -c)
            if [ "$hash_len" -eq "41" ]; then
                saasherder --context $context --environment production update $INSECURE hash $service master
                if [ $? -ne 0 ]; then
                    rc=1
                fi
            fi
        done

        saasherder --context $context --environment production pull $TOKEN $INSECURE
        if [ $? -ne 0 ]; then
            rc=1
        fi

        saasherder --context $context --environment production template --local tag
        if [ $? -ne 0 ]; then
            rc=1
        fi
    done
done

exit $rc
