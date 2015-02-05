#!/usr/bin/env/python
#-*- coding:utf-8 -*-

import os

N = 30

PATH = "/home/xlore/Xlore/etc/ttl/"
INSTANCE_PAGERANK = os.path.join(PATH, "xlore.instance.pagerank.dat")
#http://en.wikipedia.org/w/index.php?title=Wikipedia:Version_0.7/Popular_pages&action=edit&section=1
INSTANCE_WIKI_TOP = os.path.join("wiki_top_articles.dat")
INSTANCE_LIST = os.path.join(PATH, "xlore.instance.list.ttl")
INSTANCE_MENTION = os.path.join(PATH, "xlore.instance.mention.ttl")
INSTANCE_INFOBOX = os.path.join(PATH, "xlore.instance.infobox.ttl")
INSTANCE_TAXONOMY = os.path.join(PATH, "xlore.taxonomy.ttl")
INSTANCE_REFERENCE = os.path.join(PATH, "xlore.instance.reference.ttl")

#def get_top_instances(fn):
#    l = []
#    for line in open(fn):
#        l.append(line.strip('\n').split(','))
#    l = sorted(l, key=lambda x:x[1], reverse=True)
#    result = [k for k,v in l[:N]]
#    del l
#    return result

def get_top_instances(fn, inslist):
    print fn
    print inslist
    labels = []
    result = set()
    for line in open(fn):
        if "[[:" in line:
            l = line[line.index("[[:")+3:-3]
            print l
            labels.append(l)

    for line in open(inslist):
        if not line.startswith('<'):
            continue
        if "rdfs:label" in line:
            label = line.split('"')[1]
            if label in labels:
                i = line[1:line.index('>')]
                result.add(i)
       
    return list(result)

def label_stat(ins, fn):
    print fn
    i_label = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')]
        if i in ins:
            if "rdfs:label" in line:
                label = line.split('"')[1]
                l = i_label.get(i,"")
                if len(l) == 0:
                    i_label[i] = label
                else:
                    i_label[i] = l+"::;"+label
    return i_label

def mention_stat(ins, fn):
    print fn
    i_c = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')]
        if i in ins:
            i_c[i] = i_c.get(i,0)+1
    return i_c

def property_stat(ins, fn):
    print fn
    i_prop = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')].split('/')[-1]
        if "/property/" in line and not "/concept/" in line:# type
            if i in ins:
                i_prop[i] = i_prop.get(i,0)+1
    return i_prop

def type_related_classes_stat(ins, fn):
    print fn
    i_type = {}
    i_related = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')].split('/')[-1]
        if "owl:InstanceOf" in line and "concept" in line:# type
            if i in ins:
                i_type[i] = i_type.get(i,0)+1
        if "property#isRelatedTo" in line and "concept" in line: #related classes
            if i in ins:
                i_related[i] = i_related.get(i,0)+1
    return i_type, i_related

def related_instances_stat(ins, fn):
    print fn
    i_c = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')]
        if i in ins:
            i_c[i] = i_c.get(i,0)+1
    return i_c


if __name__=="__main__":
    #ins = get_top_instances(INSTANCE_PAGERANK)
    ins = get_top_instances(INSTANCE_WIKI_TOP,INSTANCE_LIST)
    print "ins:",ins
    label = label_stat(ins, INSTANCE_LIST)
    print "label:",label
    ttype, related_class = type_related_classes_stat(ins, INSTANCE_TAXONOMY)
    print "type:",ttype
    print "related class:",related_class
    mention = mention_stat(ins, INSTANCE_MENTION)
    print "mention:",mention
    prop = property_stat(ins, INSTANCE_INFOBOX)
    print "property",prop
    related_ins =  related_instances_stat(ins, INSTANCE_REFERENCE)
    print "related instance:",related_ins
    with open('instance-statistics.txt','w') as f:
        for i in ins:
            f.write("%s^^%s^^%d^^%d^^%d^^%d^^%d**\n"%(i, label[i], ttype.get(i,0), mention.get(i,0), related_class.get(i,0), prop.get(i,0), related_ins.get(i,0)))

        
