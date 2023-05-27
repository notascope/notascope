#!/bin/zsh

{echo "import hvplot.pandas; hvplot.extension('matplotlib'); "; cat $1 ;  echo "hvplot.save(p, filename='$2.png')"} | python
