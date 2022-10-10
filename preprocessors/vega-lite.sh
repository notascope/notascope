#!/bin/zsh

cat $1 | jq 'del(..|.data?)' | jq 'del(.datasets)' |  jq -c 'del(.description)'  > $2
