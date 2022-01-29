#!/bin/zsh

{cat $1 ; echo "fig.write_image('$2')"} | python
