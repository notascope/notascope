#!/bin/zsh

{cat $1 ; echo "from bokeh.io import export_svg; p.output_backend = 'svg'; export_svg(p, filename='$2.svg')"} | python
