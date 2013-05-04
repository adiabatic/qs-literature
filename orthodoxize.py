# coding: UTF-8

import xml.etree.ElementTree as ET
import os
from os.path import join
newnames = [
    u"The Call of Cthulhu",
    u"1. The Horror in Clay",
    u"2. The Tale of Inspector Legrasse",
    u"3. The Madness from the Sea"
]

DIR = 'call-of-cthulhu.d'

NAVFILE = join(DIR, 'nav.xhtml')
TITLEPAGE = join(DIR, 'title_page.xhtml')
OPF = join(DIR, 'content.opf')


def fix_nav_file():
    ET.register_namespace('', "http://www.w3.org/1999/xhtml")
    ET.register_namespace('epub', "http://www.idpf.org/2007/ops")

    nt = ET.parse(NAVFILE)
    ntr = nt.getroot()
    rewriteables = ntr.findall(".//{http://www.w3.org/1999/xhtml}span")

    for elem, newname in zip(rewriteables, newnames):
        elem.text = newname

    titles = ntr.findall(".//{http://www.w3.org/1999/xhtml}h1")
    for title in titles:
        title.text = u"The Call of Cthulhu"


    nt.write(NAVFILE)

fix_nav_file()

def remove_title_page():
    """
    Remove the title page and all references to it in the content.opf.
    """
    ET.register_namespace('', "http://www.idpf.org/2007/opf")
    ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")
    os.remove("call-of-cthulhu/title_page.xhtml")
    opf = ET.parse(OPF)
    opfr = opf.getroot()
    
    for manifest in opfr.findall('.//{http://www.idpf.org/2007/opf}manifest'):
        for deletable in opfr.findall('.//{http://www.idpf.org/2007/opf}item[@id="title_page"]'):
            manifest.remove(deletable)

    for spine in opfr.findall('.//{http://www.idpf.org/2007/opf}spine'):
        for deletable in opfr.findall('.//{http://www.idpf.org/2007/opf}itemref[@idref="title_page"]'):
            spine.remove(deletable)
    
    opf.write(OPF)
    
#remove_title_page()
