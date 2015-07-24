#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
Replace property label in infoboxes by display label in template of Wikipedia.
"""

import codecs
OLD="/home/xlore/disk2/raw.wiki/zhwiki-infobox.dat"
NEW="/home/xlore/disk2/raw.wiki/zhwiki-infobox-new.dat"
TEMPLATE="/home/xlore/server36/infobox/zhwiki-template-triple.dat"

tem_tl_dl = {} # tem_tl_dl[template][template label][display label]

for line in open(TEMPLATE):
    tem, tl, _, dl = line.strip('\n').split('\t')
    tem_tl_dl[tem.strip('Template:')][tl] = dl

f = codecs.open(NEW,'w')

count = 0
for line in open(OLD):
    title, info = line.split('\t\t')
    if len(info): #if infobox exists
        tem, text = info.split(':::::')
        if tem in tem_tl_dl:
            print "Hit Template:%s"%tem
            infos = []
            for b in text.split('::::;'):
                k,v = b.split('::::=')
                if k in tem_tl_dl[tem]:
                    k = tem_tl_dl[tem][k]
                infos.append((k,v))
            infs = ['::::='.join(i) for i in infos]
            line = "%s:::::%s\n"%(tem, '::::;'.join(infs))
    f.write(line)
    f.flush()
f.close()

