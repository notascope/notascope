#!/bin/bash

cp $1 $2 && R CMD BATCH --vanilla --no-echo <(echo "library(formatR); tidy_file('$2')") /dev/null
