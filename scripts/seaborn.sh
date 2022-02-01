#!/bin/zsh

{cat $1 ; echo "fig.figure.savefig('$2')"} | python
