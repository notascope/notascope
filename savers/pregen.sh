#!/bin/zsh

indir=$(dirname $1)
infile=$(basename $1)
inslug="${infile%%.*}"
outdir=$(dirname $2)

cp $indir/img/$inslug.* $outdir
