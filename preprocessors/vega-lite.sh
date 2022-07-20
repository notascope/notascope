#!/bin/zsh

cat $1 | jq 'del(..|.data?)' | jq 'del(.datasets)' |  jq 'del(.description)'  > $2
