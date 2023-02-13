#!/bin/bash
set -e
cp $1 $2
R CMD BATCH --vanilla --no-echo <(echo "library(formatR); library(styler); tidy_file('$2',width.cutoff = I(80)); style_file('$2');") /dev/null
