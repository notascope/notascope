#!/bin/zsh

cat $1 | sed '/^[a-z]*$/d' | isort - --profile=black | black - -C -q -l 60 > $2
