#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
Replace property label in infoboxes by display label in template of Wikipedia.
"""

import codecs
import re

OLD="/home/xlore/disk2/raw.wiki/zhwiki-infobox.dat"
NEW="/home/xlore/disk2/raw.wiki/zhwiki-infobox-new.dat"
TEMPLATE="/home/xlore/server36/infobox/zhwiki-template-triple.dat.uniq.bak"
#OLD="/home/xlore/disk2/raw.wiki/enwiki-infobox.dat"
#NEW="/home/xlore/disk2/raw.wiki/enwiki-infobox-new.dat"
#TEMPLATE="/home/xlore/server36/infobox/enwiki-template-triple.dat.uniq.bak"

tem_tl_dl = {} # tem_tl_dl[template][template label][display label]

for line in open(TEMPLATE):
    tem, tl, _, dl = line.strip('\n').split('\t')
    tem = tem.replace('Template:','').lower()
    if not tem in tem_tl_dl:
        #print tem
        tem_tl_dl[tem] = {}
    tem_tl_dl[tem][tl.lower()] = dl

f = codecs.open(NEW,'w')

count = 0
for line in open(OLD):
    if len(line.split('\t\t')) == 2:#if infobox exists
        title, info = line.split('\t\t')
        tem, text = info.split(':::::',1)
        if tem in tem_tl_dl:
            #print "%s Hit Template:%s"%(title, tem)
            infos = []
            for b in text.split('::::;'):
                k,v = b.split('::::=',1)
                lk = k.lower()
                if lk in tem_tl_dl[tem]:
                    nk = tem_tl_dl[tem][lk]
                    for i in re.findall(r"\[\[(.*?)\]\]",nk):
                        j = i
                        i = '[['+i+']]'
                        if '|' in j:
                            j = j.split('|')[0]
                        #print "Replace i:%s by j:%s"%(i,j)
                        nk = nk.replace(i, j)
                else:
                   nk = k
                infos.append((nk,v))
            infs = ['::::='.join(i) for i in infos]
            line = "%s\t\t%s:::::%s"%(title, tem, '::::;'.join(infs))
    f.write(line)
    f.flush()
f.close()

