#!/bin/zsh

{echo "import holoviews as hv; hv.extension('matplotlib'); "; cat $1 ;  echo "hv.save(p, filename='$2.png')"} | python
