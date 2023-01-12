#!/bin/zsh

cat $1 | jq 'del(..|.data?.values?)' | jq 'del(.datasets)' |  jq 'del(.description)'  > $2
