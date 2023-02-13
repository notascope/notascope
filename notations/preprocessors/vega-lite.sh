#!/bin/zsh

cat $1 | jq 'del(..|.data?.values?)' | jq 'del(.datasets)' |  jq 'del(.description)' | jq -c -S > $2
