# coding: UTF-8

from os.path import join
import json

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
