# coding: UTF-8

import sys
import json
import codecs

from workinfo import WorkInfo



def generate_dc_metadata(wi):
    ss = []
    ins =  "author  year rights".split()
    outs = "creator date rights".split()
    
    for i, o in zip(ins, outs):
        ov = wi.metadata.get(i)
        if ov:
            ss.append(u"<dc:{}>{}</dc:{}>".format(o, ov, o))

    contributors = wi.metadata.get('contributors', [])
    for contributor in contributors:
        ss.append(u"<dc:contributor>{}</dc:contributor>".format(contributor))  
    
    s = u'\n'.join(ss)
    with codecs.open(wi.prefix + ".dcmetadata.xml", "w") as f:
        f.write(s)

for basename in sys.argv[1:]:
    wi = WorkInfo(basename)
    generate_dc_metadata(wi)
