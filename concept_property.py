# -*- coding=utf-8 -*-

import os
import codecs

DIR = "/home/xlore/XloreData/etc/ttl"
CONCEPT_INSTANCE = os.path.join(DIR,"xlore.taxonomy.ttl")
INSTANCE_PROPERTY = os.path.join(DIR,"xlore.instance.infobox.ttl")
CONCEPT_PROPERTY_FREQUENCY = os.path.join(DIR,"xlore.concept.property.frequency.dat")

ins_pro = {} #k:ins id, v: pro id list
domain_pro = {}
con_pro = {} 

print "Reading %s ..."%INSTANCE_PROPERTY
count = 0
for line in codecs.open(INSTANCE_PROPERTY):
    if line.startswith('<http://xlore.org/instance/'):
        count += 1
        if count % 100000 == 0:
            print count
        i,p,t = line.split(" ",2) 
        i = i.rsplit("/",1)[-1][:-1]
        p = p.rsplit("/",1)[-1][:-1]
        ins_pro[i] = ins_pro.get(i,[]) + [p]

print "Reading %s ..."%INSTANCE_PROPERTY
count = 0
for line in codecs.open(INSTANCE_PROPERTY):
    if line.startswith('<http://xlore.org/property/'):
        count += 1
        if count % 100000 == 0:
            print count
        p,o,c = line.split(" ",2) 
        if "isDefinedBy" in o:
            c = c.rsplit("/",1)[-1]
            c = c[:c.index('>')]
            p = p.rsplit("/",1)[-1][:-1]
            if not con_pro.has_key(c):
                con_pro[c] = {}
            con_pro[c].update({p:0})

print "Reading %s ..."%CONCEPT_INSTANCE
count = 0
for line in codecs.open(CONCEPT_INSTANCE):
    if line.startswith('<http://xlore.org/instance/'):
        count += 1
        if count % 100000 == 0:
            print count
        i,r,c = line.split(' ',2)
        i = i.rsplit("/",1)[-1][:-1]
        c = c.rsplit("/",1)[-1]
        c = c[:c.index('>')]
        pros = ins_pro.get(i,[])
        for p in pros:
            #p_count = con_pro.get(c, {})
            #p_count[p] = p_count.get(p, 0) + 1
            #con_pro[c] = p_count
            if con_pro.has_key(c) and con_pro[c].has_key(p):
                con_pro[c][p] = con_pro[c].get(p,0) + 1
            
print "Writing result..."
with codecs.open(CONCEPT_PROPERTY_FREQUENCY, "w") as fw:
    for c, p_fre in con_pro.items():
        for p, f in sorted(p_fre.items(), key=lambda x:x[1], reverse=True):
            fw.write("%s\t%s\t%d\n"%(c,p,f))

