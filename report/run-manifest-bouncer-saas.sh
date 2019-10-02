#!/bin/bash

WORKDIR="$PWD/saas-repos"

find "${WORKDIR}" -path '*-processed/*.yaml' -type f | while read manifest; do
    OUTPUT="$(manifest-bouncer --enable-limits --enable-requests $manifest)"
    if [ -n "$OUTPUT" ]; then
        echo "-- ${manifest##$WORKDIR/} --"
        echo "$OUTPUT"
        echo
    fi
done
