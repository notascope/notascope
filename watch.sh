#!/bin/zsh

make -kj8 app.py
while true; do ls -d galleries/**/* | entr -dp make -kj8 app.py; sleep 1; done
