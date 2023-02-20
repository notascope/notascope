#!/bin/bash

R CMD BATCH --vanilla --no-echo  <( echo "png('$2.png'); " ; cat $1 ; echo " dev.off();") /dev/null
rm -f Rplots.pdf
