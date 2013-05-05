# coding: UTF-8

import xml.etree.ElementTree as ET
import os
from os.path import join



class WorkInfo(object):
    def __init__(self, prefix):
        self.prefix = prefix
        
        self.directory = self.prefix + '.d'
        self.navpath = join(self.directory, 'nav.xhtml')
        self.opfpath = join(self.directory, 'content.opf')
        self.titlepagepath = join(self.directory, 'title_page.xhtml')
        self.titles = []



def fix_nav_file(wi):
    ET.register_namespace('', "http://www.w3.org/1999/xhtml")
    ET.register_namespace('epub', "http://www.idpf.org/2007/ops")

    nt = ET.parse(wi.navpath)
    ntr = nt.getroot()
    rewriteables = ntr.findall(".//{http://www.w3.org/1999/xhtml}span")

    for elem, new_title in zip(rewriteables, wi.titles):
        elem.text = new_title

    titles = ntr.findall(".//{http://www.w3.org/1999/xhtml}h1")
    for title in titles:
        title.text = u"The Call of Cthulhu"

    nt.write(wi.navpath)



def remove_title_page(wi):
    """
    Remove the title page and all references to it in the content.opf.
    """
    ET.register_namespace('', "http://www.idpf.org/2007/opf")
    ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")
    os.remove("call-of-cthulhu/title_page.xhtml")
    opf = ET.parse(wi.opfpath)
    opfr = opf.getroot()
    
    for manifest in opfr.findall('.//{http://www.idpf.org/2007/opf}manifest'):
        for deletable in opfr.findall('.//{http://www.idpf.org/2007/opf}item[@id="title_page"]'):
            manifest.remove(deletable)

    for spine in opfr.findall('.//{http://www.idpf.org/2007/opf}spine'):
        for deletable in opfr.findall('.//{http://www.idpf.org/2007/opf}itemref[@idref="title_page"]'):
            spine.remove(deletable)
    
    opf.write(wi.opfpath)



coc = WorkInfo('call-of-cthulhu')
coc.titles = [
    u"The Call of Cthulhu",
    u"1. The Horror in Clay",
    u"2. The Tale of Inspector Legrasse",
    u"3. The Madness from the Sea"
]

for wi in [coc]:
    fix_nav_file(wi)
    #remove_title_page(wi)
