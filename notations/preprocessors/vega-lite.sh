#!/bin/zsh

cat $1 | jq 'del(..|.data?.values?)' | jq 'del(.datasets)' |  jq -c 'del(.description)'  > $2
