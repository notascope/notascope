#!/bin/bash

(cat $1 ; echo "ggsave('$2')") | r --no-save
