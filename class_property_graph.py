#!/usr/bin/python

import os
import sys

DIR = "/home/xlore/XloreData/etc/ttl"
CONCEPT_LIST = os.path.join(DIR, "xlore.concept.list.ttl")
PROPERTY_LIST = os.path.join(DIR, "xlore.property.list.ttl")
TAXONOMY = os.path.join(DIR, "xlore.taxonomy.ttl")
CONCEPT_PROPERTY_FREQUENCY = os.path.join(DIR, "xlore.concept.property.frequency.dat")


class ClassNode:
    def __init__(self, _id):
        self._id = None
        self.zh = None
        self.en = None
        self.children = set()
        self.properties = []

    def __repr__(self):
        return json.dumps(self.__dict__)

class Property:
    def __init__(self, _id):
        self._id = None
        self.zh = None
        self.en = None
        self.size = 0

    def __repr__(self):
        return json.dumps(self.__dict__)

def read_items(fn):
    d = {}
    for line in open(fn):
        if not "rdfs:label" in line:
            continue
        _id = line[1:line.index('>')]
        p = d.get(_id, Property(_id))
        if "@en" in line:
            p.en = line.split('"')[1]
        if "@zh" in line:
            p.zh = line.split('"')[1]
        d[_id] = p
    return d

class Graph:
    def __init__(self, confn, propfn, con_prop_fn, taxonomy_fn):
        self.graph = self.generate_graph(confn, propfn, con_prop_fn, taxonomy_fn)

    def generate_graph(self, confn, propfn, con_prop_fn, taxonomy_fn):
        cons = read_items(confn)
        props = read_items(propfn)
    
        graph = {}
        for line in open(con_prop_fn):
            con, prop, c = line.split('\t')
            graph[con] = graph.get(con, ClassNode(con))
            graph[con].zh = cons[con].zh
            graph[con].en = cons[con].en
            p = props[prop]
            p.size = int(c)
            graph[con].properties.append(p)
    
        for line in open(taxonomy_fn):
            if line.startswith('<http://xlore.org/concept/') and 'owl:SubClassOf' in line:
                sub,relation,c = line.split(' ',2)
                sub = sub.rsplit("/",1)[-1][:-1]
                c = c.rsplit("/",1)[-1]
                c = c[:c.index('>')]
                if not sub in graph:
                    continue
                parent = graph.get(c, ClassNode(c))
                parent.children.add(sub)
                graph[c] = parent
        del cons
        del props

    def get_subgraph(self, keyword_id):
        return self.graph(keyword_id, None)

if __name__ == '__main__':
    graph = Graph(CONCEPT_LIST, PROPERTY_LIST, CONCEPT_PROPERTY_FREQUENCY, TAXONOMY)
    #41 Film
    while True:
        keyword_id = sys.stdin
        print graph.get_subgraph(keyword_id)
        

