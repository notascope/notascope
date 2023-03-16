#!/bin/zsh

{cat $1 ; echo "from altair_saver import save; save(chart, '$2.svg', method='node')"} | python
