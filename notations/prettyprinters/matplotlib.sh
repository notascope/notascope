#!/bin/zsh

cat $1 | sed '/^[a-z]*$/d' | isort - --profile=black | black - -C -q > $2
