#!/bin/zsh

{cat $1 ; echo "from bokeh.io import export_png; export_png(p, filename='$2.png')"} | python
