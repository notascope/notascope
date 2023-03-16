#!/bin/zsh

{cat $1 ; echo "chart.properties(width=400, height=400).save('$2.svg')"} | python
