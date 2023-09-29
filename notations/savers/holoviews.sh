#!/bin/zsh

{cat $1 ;  echo "hv.save(p, filename='$2.png', size=200)"} | python
