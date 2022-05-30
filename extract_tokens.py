import sys
import re

# this script extracts leaves from the output of `gumtree parse`

last_indent = None
last_line = None
for line in sys.stdin:
    line = line.rstrip()
    indent = len(line) - len(line.lstrip())
    if last_indent is not None and indent <= last_indent:
        print(last_line)
    last_indent = indent
    last_line = re.search("(.*) \[.*\]$", line).group(1).strip()
print(last_line)
