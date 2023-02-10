#!/bin/zsh

{cat $1 ; echo "fig.write_image('$2.png')"} | python
#sed -i '' 's/vector-effect: non-scaling-stroke;//g' $2.svg
