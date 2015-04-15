#!/usr/bin/python
#-*- coding:utf-8 -*-

#FILE1 = "/home/xlore/Xlore/etc/ttl/hudong.icon.ttl"
#FILE2 = "/home/xlore/Xlore/etc/ttl/xlore.instance.icon.hudong.ttl"
FILE1 = "/home/lmy/XLore/enwiki.icon.ttl"
FILE2 = "/home/xlore/Xlore/etc/ttl/xlore.instance.icon.enwiki.ttl"
OUTPUT = FILE2+".new"

def merge_images(FILE1, FILE2):
    d1 = dict((int(line.split()[0][1:-1]), line) for line in open(FILE1) if line.startswith('<'))
    d2 = dict((int(line.split()[0][1:-1]), line) for line in open(FILE2) if line.startswith('<'))
    d1.update(d2)
    return d1

def generate_ttl(d):
    with open(OUTPUT,'w') as f:
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
        
        for k,v in sorted(d.items()):
            f.write(v)

if __name__=="__main__":
    d = merge_images(FILE1, FILE2)
    generate_ttl(d)
