#!/bin/zsh

{cat $1 ; echo "ax.figure.savefig('$2.png')"} | python
