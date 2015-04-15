#!/usr/bin/python
#-*- coding:utf-8 -*-

import os

PATH = "/home/xlore/Xlore/etc/ttl/"
INSTANCE_LIST = os.path.join(PATH, "xlore.instance.list.ttl")
CONCEPT_LIST = os.path.join(PATH, "xlore.concept.list.ttl")
PROPERTY_LIST = os.path.join(PATH, "xlore.property.list.ttl")
OUTPUT = "data/en_zh.txt"

def get_en_zh_label(fn):
    fo = open(OUTPUT,'a')
    with open(fn) as f:
        i = 1
        d = []
        line = f.readline()
        while line:
            if "rdf:type" in line:
                d = []
            if "rdfs:label" in line:
                first = line.index('"')+1
                d.append(line[first: line.rindex('"')])
                if len(d) == 2:
                    fo.write(d[0]+"\t"+d[1]+"\n")
                    fo.flush()
            line = f.readline()
    fo.close()

if __name__ == "__main__":
    get_en_zh_label(INSTANCE_LIST)
    get_en_zh_label(CONCEPT_LIST)
    #get_en_zh_label(PROPERTY_LIST)


