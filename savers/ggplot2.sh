#!/bin/bash

R CMD BATCH --vanilla --no-echo <(cat $1 ; echo "ggsave('$2.svg')") /dev/null
