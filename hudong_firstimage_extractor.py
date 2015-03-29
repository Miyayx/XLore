#!/usr/bin/python
#-*- coding:utf-8 -*-

from firstimage_extractor import *

HUDONG_DUMP='/home/xlore/disk2/data/hudong/hudong-dump-20120823.dat'
OUTPUT = 'hudong.firstimage.dat'
TTL = '/home/xlore/Xlore/etc/ttl/xlore.instance.icon.hudong.ttl'
INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'

class HudongFirstImage(FirstImage):

    #def __init__(self, i, o, ttl):
    #    super(i, o, ttl)

    def extract(self):
        title = ""
        image = ""
        with open(self.output,'w') as f:
            for line in open(self.input):
                if line.startswith('Title:'):
                    title = line.strip('\n').split(':')[-1]
                if line.startswith('Image:'):
                    image = line.strip('\n').split(':',1)[-1].split('::;')[0]
                    if not 'http://a0.att.hudong.com/00/00/404.jpg' == image:
                        f.write('%s\t%s\n'%(title,image))
                        f.flush()
    
    def generate_ttl(self):
        with open(self.ttl,'w') as f:
            f.write('@base <http://xlore.org/instance/> .\n')
            f.write('@prefix property: <http://xlore.org/property#> .\n')
            f.write('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n')
            f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
            f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
            f.write('\n')
            f.write('property:hasIcon rdf:type rdf:Property .\n')
            f.write('property:hasIcon rdf:type owl:DatatypeProperty .\n')
            f.write('property:hasIcon rdfs:label "hasIcon" .\n')
            f.write('property:hasIcon rdfs:domain owl:Individual .\n')
            f.write('\n')
            f.flush()
    
            for line in open(INSTANCE_LIST):
                if '@zh' in line:
                    i = line[0:line.index(' ')]
                    title = line[line.index('"')+1:line.rindex('"')]
                    if title in images:
                        f.write('%s property:hasIcon "%s"@hudong .\n'%(i,images[title]))
                        f.flush()

if __name__=="__main__":
    fi = HudongFirstImage(HUDONG_DUMP, OUTPUT, TTL)
    fi.run()

