#!/bin/zsh

cat $1 | jq '. + {width: 400, height: 400}' | node_modules/vega-lite/bin/vl2png > $2.png
