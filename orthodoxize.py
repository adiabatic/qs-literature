# coding: UTF-8

import xml.etree.ElementTree as ET
import os
from os.path import join
from shutil import copyfile
import sys
import json
import codecs



class WorkInfo(object):
    def __init__(self, prefix):
        self.prefix = prefix
        
        self.directory = self.prefix + '.d'
        self.navpath = join(self.directory, 'nav.xhtml')
        self.opfpath = join(self.directory, 'content.opf')
        self.titlepagepath = join(self.directory, 'title_page.xhtml')
        self.itmfilename = self.prefix + ".iTunesMetadata.plist"
        self.itmpath = join(self.directory, "iTunesMetadata.plist")
        self.metadata = {}

        try:
            with open(self.prefix + '.json') as f:
                metadata = json.load(f)
                if metadata:
                    self.metadata = metadata
        except IOError as e:
            print "I/O error({}): {}".format(e.errno, e.strerror)
                
        self.titles = self.metadata.get('titles', [])
        


def fix_nav_file(wi):
    """
    Change the titles in nav.xhtml to Orthodox (listed in wi.titles)
    """
    ET.register_namespace('', "http://www.w3.org/1999/xhtml")
    ET.register_namespace('epub', "http://www.idpf.org/2007/ops")

    nt = ET.parse(wi.navpath)
    ntr = nt.getroot()
    rewriteables = ntr.findall(".//{http://www.w3.org/1999/xhtml}span")

    for elem, new_title in zip(rewriteables, wi.titles):
        elem.text = new_title

    if wi.titles:
        for title in ntr.findall(".//{http://www.w3.org/1999/xhtml}h1"):
            title.text = wi.titles[0]

    nt.write(wi.navpath)



def remove_title_page(wi):
    """
    Remove the title page and all references to it in the content.opf.
    """
    os.remove(wi.titlepagepath)

    # That was easy! Now, let’s remove it _from the OPF_…
    ET.register_namespace('', "http://www.idpf.org/2007/opf")
    ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")
    opf = ET.parse(wi.opfpath)
    opfr = opf.getroot()

    
    for manifest in opfr.findall('.//{http://www.idpf.org/2007/opf}manifest'):
        for deletable in opfr.findall('.//{http://www.idpf.org/2007/opf}item[@id="title_page"]'):
            manifest.remove(deletable)

    for spine in opfr.findall('.//{http://www.idpf.org/2007/opf}spine'):
        for deletable in opfr.findall('.//{http://www.idpf.org/2007/opf}itemref[@idref="title_page"]'):
            spine.remove(deletable)
    
    opf.write(wi.opfpath)


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
      



def add_itunes_metadata(wi):
    
    copyfile(wi.itmfilename, wi.itmpath)
    
    ET.register_namespace('', "http://www.idpf.org/2007/opf")
    ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")
    opf = ET.parse(wi.opfpath)
    opfr = opf.getroot()
    
    attribs = {
        'id': 'itunesmetadata',
        'href': 'iTunesMetadata.plist',
        'media-type': 'application/xml'
    }
    itme = ET.Element('{http://www.idpf.org/2007/opf}item', attribs)
    
    for manifest in opfr.findall('.//{http://www.idpf.org/2007/opf}manifest'):
        manifest.append(itme)
        
    opf.write(wi.opfpath)



for basename in sys.argv[1:]:
    wi = WorkInfo(basename)
    
    fix_nav_file(wi)
    remove_title_page(wi)
    generate_dc_metadata(wi)
    add_itunes_metadata(wi)
