#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
获取wiki 的 FirstImage： 
1. 从infobox里获得image信息 
2.  根据wiki提供的api获得json，从json中提取准确的image url
* 
注：本代码负责第2步,第一步由WikiExtractor中的FirstImageExtractor完成

Example：
http://en.wikipedia.org/w/index.php?action=raw&title=Douglas_Jardine
    image = Douglas Jardine Cigarette Card.jpg 
    image_size = 175px
图片对应json数据:
    http://en.wikipedia.org/w/api.php?action=query&titles=File:Douglas_Jardine_Cigarette_Card.jpg&prop=imageinfo&iiprop=url
"""

"""
获得raw数据的wiki api
http://zh.wikipedia.org/w/index.php?action=raw&title=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6
http://en.wikipedia.org/w/index.php?action=raw&title=Douglas_Jardine

获得image json的api
http://zh.wikipedia.org/w/api.php?action=query&titles=File:Tsinghua_University_Logo.svg&prop=imageinfo&iiprop=url&format=json
http://en.wikipedia.org/w/api.php?action=query&titles=File:Douglas_Jardine_Cigarette_Card.jpg&prop=imageinfo&iiprop=url
"""

ENAPI = "http://en.wikipedia.org/w/api.php?action=query&titles=File:%s&prop=imageinfo&iiprop=url&format=json"

from firstimage_extractor import *
import json
import urllib
import codecs

INPUT="/home/xlore/disk2/raw.wiki/enwiki-firstimage.dat"
OUTPUT="data/enwiki.firstimage.dat"
TTL = '/home/xlore/Xlore/etc/ttl/xlore.instance.icon.enwiki.ttl'
INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
SEPERATOR="\t\t"

class EnwikiFirstImage(FirstImage):

    def extract(self):
        title = ""
        image = ""
        with codecs.open(self.output, 'w', 'utf-8') as f:
            for line in open(self.input):
                try:
                    title, img = line.split('\t\t')
                except:
                    continue
                if len(img.strip()) == 0:
                    continue
                img = '_'.join(img.split())
                try:
                    j = urllib.urlopen(ENAPI%img).read()
                    image = json.loads(j)['query']['pages'].values()[0]['imageinfo'][0]['url']
                except:
                    continue
                #print title,image
                f.write('%s\t%s\n'%(title.decode('utf-8'),image ))
                f.flush()
    
    def generate_ttl(self, images):
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
                        f.write('%s property:hasIcon "%s"@enwiki .\n'%(i,images[title]))
                        f.flush()

if __name__=="__main__":
    fi = EnwikiFirstImage(INPUT, OUTPUT, TTL)
    fi.run()
