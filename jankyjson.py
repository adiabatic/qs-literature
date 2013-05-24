# coding: UTF-8

"""
usage:
jankyjson.py [file] [selector]

"""

# Consider using <http://stedolan.github.io/jq/> for Serious Work™.

import sys
import json
import re

ARRAY_ACCESS = re.compile(r"([\w-]+)\[(\d+)\]")


if len(sys.argv) != 3:
    sys.stderr.write(__doc__+'\n')
    sys.exit(1)

fn = sys.argv[1]
selector = sys.argv[2]
r = u''

with open(fn) as f:
    j = json.load(f)
    try:
        m = ARRAY_ACCESS.match(selector)
        if m:
            r = j[m.group(1)][int(m.group(2))]
        else:
            r = j[selector]
    except KeyError as e:
        sys.stderr.write(u"couldn’t find key “{}” in file “{}”\n".format(selector, fn))

    sys.stdout.write(r.encode('UTF-8'))
