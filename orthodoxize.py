# coding: UTF-8

import xml.etree.ElementTree as ET
import os
from os.path import join
from shutil import copyfile
import sys
import json
import codecs
import plistlib
from workinfo import WorkInfo
        


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



      

def generate_plist(wi):
    d = {
        'artistName': wi.metadata['author'],
        'sort-artist': wi.metadata['author-sort'],
        'sort-artist-status': 1,

        'releaseDate': unicode(wi.metadata['year']),
        'year': unicode(wi.metadata['year']),

        'genre': wi.metadata['genre'],
        
        'itemName': wi.metadata['titles'][0],
        'playlistName': wi.metadata['titles'][0],
        
        'book-info': {'mime-type':"application/epub+zip"}            
    }
    
    plistlib.writePlist(d, wi.itmpath)

def add_itunes_metadata(wi):
    
    generate_plist(wi)
    
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
#    remove_title_page(wi)
    generate_dc_metadata(wi)
    add_itunes_metadata(wi)
