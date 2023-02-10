#!/bin/bash

R CMD BATCH --vanilla --no-echo <(cat $1 ; echo " ggsave('$2.png');") /dev/null
rm -f Rplots.pdf
