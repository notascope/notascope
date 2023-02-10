#!/bin/zsh

{cat $1 ; echo "p.save('$2.png') if hasattr(p, 'save') else p.figure.savefig('$2.png')"} | python
