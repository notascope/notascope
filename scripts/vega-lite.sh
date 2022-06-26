#!/bin/zsh

echo "import altair as alt; alt.Chart.from_json(open('$1', 'r').read()).save('$2.svg')" | python
