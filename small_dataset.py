#!/env/bin/python
# -*- coding:utf-8 -*-

import os

DIR = "/home/xlore/XloreData/etc/ttl"
ODIR = "/home/lmy/XLore/data/small"

N1=50000
N2=50000
N3=10000

def small_instance(fn, ofn):
    fw = open(ofn, 'w')
    for line in open(fn):
        if not line.startswith('<'):
            fw.write(line)
        i = line[1:line.index('>')]
        if int(i) <= N1:
            fw.write(line)
    fw.close()

def small_concept(fn, ofn):
    small_instance(fn, ofn)
    
def small_property(fn, ofn):
    fw = open(ofn, 'w')
    for line in open(fn):
        if not line.startswith('<'):
            fw.write(line)
        i = line[1:line.index('>')]
        if int(i) <= N3:
            fw.write(line)
    fw.close()

def small_taxonomy(fn, ofn):
    fw = open(ofn, 'w')
    for line in open(fn):
        if not line.startswith('<'):
            fw.write(line)
        i, _, j = line.strip('\n').split()
        i = i.split('/')[-1]
        j = j.split('/')[-1]
        if int(i) <= N1 and int(j) <= N1 :
            fw.write(line)
    fw.close()

def small_infobox(fn, ofn):
    fw = open(ofn, 'w')
    for line in open(fn):
        if not line.startswith('<'):
            fw.write(line)
        i, p, j = line.strip('\n').split()
        if j.startswith('<'):
            j = j.split('/')[-1]
            if int(j) > N1:
                continue
        i = i.split('/')[-1]
        p = p.split('/')[-1]
        if int(i) <= N1 and int(p) <= N1 :
            fw.write(line)
    fw.close()

def small_instance_ref(fn, ofn ):
    fw = open(ofn, 'w')
    for line in open(fn):
        if not line.startswith('<'):
            fw.write(line)
        i, _, j = line.strip('\n').split()
        i = i[1:-1]
        j = j[1:-1]
        if int(i) <= N1 and int(j) <= N1 :
            fw.write(line)
    fw.close()

def small_instance_url(fn, ofn):
    small_instance(fn, ofn)

def small_instance_mention(fn, ofn):
    small_instance(fn, ofn)

if __name__=="__main__":
    small_instance(os.path.join(DIR, 'xlore.instance.list.ttl'), os.path.join(ODIR, "xlore.instance.list.small.ttl"))
    small_concept(os.path.join(DIR, 'xlore.concept.list.ttl'), os.path.join(ODIR, "xlore.concept.list.small.ttl"))
    small_property(os.path.join(DIR, 'xlore.property.list.ttl'), os.path.join(ODIR, "xlore.property.list.small.ttl"))
    small_taxonomy(os.path.join(DIR, 'xlore.taxonomy.ttl2'), os.path.join(ODIR, "xlore.taxonomy.small.ttl"))
    small_infobox(os.path.join(DIR, 'xlore.instance.infobox.ttl7'), os.path.join(ODIR, "xlore.instance.infobox.small.ttl"))
    small_instance_ref(os.path.join(DIR, 'xlore.instance.reference.ttl'), os.path.join(ODIR, "xlore.instance.reference.small.ttl"))
    small_instance_url(os.path.join(DIR, 'xlore.instance.url.ttl'), os.path.join(ODIR, "xlore.instance.url.small.ttl"))
    small_instance_mention(os.path.join(DIR, 'xlore.instance.mention.ttl'), os.path.join("xlore.instance.mention.small.ttl"))


