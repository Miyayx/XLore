#!/usr/bin/env/python
#-*- coding:utf-8 -*-

import os

N = 30

PATH = "/home/xlore/Xlore/etc/ttl/"
PROPERTY_LIST = os.path.join(PATH, "xlore.property.list.ttl")
INSTANCE_INFOBOX = os.path.join(PATH, "xlore.instance.infobox.ttl")

def get_top_properties(fn):
    d = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        if "/property/" in line and "/instance/" in line:#instance 
            p = line.split()[1]
            i = p[1:p.index('>')].split('/')[-1]
            d[i] = d.get(i,0)+1
    d = sorted(d.items(), key=lambda x:x[1], reverse=True)
    result = [k for k,v in d[:N]]
    del d
    return result

def label_stat(props, fn):
    print fn
    i_label = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')]
        if i in props:
            if "rdfs:label" in line:
                label = line.split('"')[1]
                l = i_label.get(i,"")
                if len(l) == 0:
                    i_label[i] = label
                else:
                    i_label[i] = l+"::;"+label
    return i_label

def infobox_stat(props, fn):
    print fn
    i_type = {}
    i_domain = {}
    i_range = {}
    i_ins = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        if "/property/" in line and "/instance/" in line:#instance 
            p = line.split()[1]
            i = p[1:p.index('>')].split('/')[-1]
            if i in props:
                i_ins[i] = i_ins.get(i,0)+1
        else:
            i = line[1:line.index('>')].split('/')[-1]
            if i in props:
                if "rdf:type" in line: #type
                    t = line[line.index('owl:')+4:-2]
                    print t
                    i_type[i] = t
                if "concept" in line and ("property#hasValueFrom" in line): #range
                    i_range[i] = i_range.get(i,0)+1
                if "property#isDefinedBy" in line: #domain
                    i_domain[i] = i_domain.get(i,0)+1

    return i_type, i_domain, i_range, i_ins


if __name__=="__main__":
    props = get_top_properties(INSTANCE_INFOBOX)
    print "props:",props
    label = label_stat(props, PROPERTY_LIST)
    print "label:",label
    ttype, domain, range, ins = infobox_stat(props, INSTANCE_INFOBOX)
    print "type:",ttype
    print "domain:",domain
    print "range:",range
    print "ins:",ins
    with open('property-statistics.txt','w') as f:
        for i in props:
            f.write("%s^^%s^^%s^^%d^^%d^^%d**\n"%(i, label[i], ttype.get(i,0), domain.get(i,0), range.get(i,0), ins.get(i,0)))

