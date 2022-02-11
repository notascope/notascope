#!/bin/zsh

{cat $1 ; echo "chart.save('$2')"} | python
