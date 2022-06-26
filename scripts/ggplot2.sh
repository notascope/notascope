#!/bin/bash

(cat $1 ; echo "ggsave('$2.svg')") | r --no-save
