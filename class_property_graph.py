#!/usr/bin/python

import os
import sys
import time
import json

DIR = "/home/xlore/XloreData/etc/ttl"
CONCEPT_LIST = os.path.join(DIR, "xlore.concept.list.ttl")
PROPERTY_LIST = os.path.join(DIR, "xlore.property.list.ttl")
TAXONOMY = os.path.join(DIR, "xlore.taxonomy.ttl")
CONCEPT_PROPERTY_FREQUENCY = os.path.join(DIR, "xlore.concept.property.frequency.dat")

class ClassNode:
    def __init__(self, _id):
        self._id = _id
        self.zh = None
        self.en = None
        self.children = []
        self.properties = []

    def __repr__(self):
        #return json.dumps(self.__dict__)
        return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True, indent=2)
        #return "zh:%s, en:%s properties:%s children:%s"%(self.zh, self.en, self.properties, self.children)

class Property:
    def __init__(self, _id):
        self._id = _id
        self.zh = None
        self.en = None
        self.size = 0

    def __repr__(self):
        #return json.dumps(self.__dict__)
        return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True)

def read_items(fn):
    print "Reading items from",fn
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
        print "Generating graph..."
        cons = read_items(confn)
        props = read_items(propfn)
    
        graph = {}
        print "Reading",con_prop_fn
        for line in open(con_prop_fn):
            con, prop, c = line.split('\t')
            graph[con] = graph.get(con, ClassNode(con))
            graph[con].zh = cons[con].zh
            graph[con].en = cons[con].en
            p = props[prop]
            p.size = int(c)
            graph[con].properties.append(p)
            #graph[con].children.append(p)
    
        print "Reading",taxonomy_fn
        for line in open(taxonomy_fn):
            if line.startswith('<http://xlore.org/concept/') and 'owl:SubClassOf' in line:
                sub,relation,c = line.split(' ',2)
                sub = sub.rsplit("/",1)[-1][:-1]
                c = c.rsplit("/",1)[-1]
                c = c[:c.index('>')]
                if not sub in graph:
                    continue
                parent = graph.get(c, ClassNode(c))
                #parent.children.append(sub)
                parent.children.append(graph[sub])
                graph[c] = parent
        del cons
        del props
        return graph

    def get_subgraph(self, keyword_id):
        fw = open("%s.json"%keyword_id, 'w')
        subgraph = self.graph.get(keyword_id, None)
        fw.write(str(subgraph))
        fw.close()
        return subgraph

    def get_bigraph_json(self, keyword_id):
        fw = open("%s.json"%keyword_id, 'w')
        subgraph = self.graph.get(keyword_id, None)
        queue = [subgraph]
        cons = []
        props = []
        edges = []
        while queue and len(cons) < 3:
             root = queue.pop(0)
             #c_id = 'c'+str(len(cons)) 
             c_i = len(cons)
             cons.append(root)
             for node in root.children:
                 if not node in cons:
                     queue.append(node)
             for prop in root.properties:
                 #p_id = props.get(prop, 'p'+str(len(props)))
                 #p_id = props.get(prop, len(props))
                 #prop_label = str(prop.zh)+str(prop.en)
                 if not prop in props:
                     props.append(prop)
                 prop.size += 1
                 p_i = props.index(prop)
                 edges.append((c_i, p_i))

        nodes = []
        for c in cons:
            clabel = ''
            if c.zh and c.en:
                clabel += (c.zh+'#'+c.en)
            elif c.zh:
                clabel += c.zh
            else:
                clabel += str(c.en)
            nodes.append({"name":clabel, "group":"concept"})
        for p in props:
            plabel = ''
            if p.zh and p.en:
                plabel += (p.zh+'#'+p.en)
            elif p.zh:
                plabel += p.zh
            else:
                plabel += str(p.en)
            print plabel,p.size
            nodes.append({"name":plabel, "group":"property"})
        
        print len(props)

        links = []
        l = len(cons)
        for e in edges:
            links.append({"source": e[0], "target":l+e[1], "value":props[e[1]].size})
        j = json.dumps({"nodes":nodes, "links":links}, indent=2)
        #print j
        
        fw.write(str(j))
        fw.close()
        return subgraph


if __name__ == '__main__':
    start = time.time()
    graph = Graph(CONCEPT_LIST, PROPERTY_LIST, CONCEPT_PROPERTY_FREQUENCY, TAXONOMY)
    print "Time Consuming:",time.time()-start

    #41 Film
    while True:
        keyword_id = raw_input()
        #print graph.get_subgraph(keyword_id)
        graph.get_bigraph_json(keyword_id)
        
