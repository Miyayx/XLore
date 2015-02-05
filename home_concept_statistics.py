#!/usr/bin/python
#-*-coding:utf-8-*-

import os

#en_concepts = ['Agriculture','Arts','Chronology','Concepts','Culture','Environment','Geography','Government','Health','History','Humanities','Humans','Language','Law','Life','Mathematics','Matter','Medicine','Nature','People','Politics','Professional studies','Science','Society','Sports','Technology','Thought','Universe']
#print "en",len(en_concepts)
ch_concepts = ['人物','自然','文化','体育','社会','历史','地理','科技','娱乐','生活','艺术','经济']
print "ch",len(ch_concepts)


PATH = "/home/xlore/Xlore/etc/ttl/"
CONCEPT_LIST = os.path.join(PATH, "xlore.concept.list.ttl")
INSTANCE_INFOBOX = os.path.join(PATH, "xlore.instance.infobox.ttl")
TAXONOMY = os.path.join(PATH, "xlore.taxonomy.ttl")
INSTANCE_REFERENCE = os.path.join(PATH, "xlore.instance.reference.ttl")

def get_top_concepts(fn):
    result = set()
    labels = set()
    for line in open(fn):
        if "rdfs:label" in line:
                label = line.split('"')[1]
                #if label in en_concepts or label in ch_concepts:
                if label in ch_concepts:
                    print label
                    print line
                    if label in labels:
                        print "@"+line
                    i = line[1:line.index('>')]
                    result.add(i)
                    labels.add(label)
    print "result",len(result)
    return result

def get_sub_concepts(top_cons, fn):
    """
    fn: taxonomy
    """
    sup_sub = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        sub = line[1:line.index('>')].split('/')[-1]
        sup = line[line.rindex('<'):line.rindex('>')].split('/')[-1]
        if "owl:SubClassOf" in line and sup in top_cons:# type
            sup_sub[sup] = sup_sub.get(sup, []) + [sub]
    return sup_sub

def label_stat(cons, fn):
    i_label = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')]
        if i in cons:
            if "rdfs:label" in line:
                label = line.split('"')[1]
                l = i_label.get(i,"")
                if len(l) == 0:
                    i_label[i] = label
                else:
                    i_label[i] = l+"::;"+label
    return i_label

def property_stat(cons, fn):
    i_prop = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')].split('/')[-1]
        if "property#isDefinedBy" in line and "/property/" in line and "/concept/" in line:# type
            if i in cons:
                i_prop[i] = i_prop.get(i,0)+1
    return i_prop

def taxonomy_stat(cons, fn):
    i_type = {}
    i_sub = {}
    i_related = {}
    i_ins = {}
    for line in open(fn):
        if not line.startswith('<'):
            continue
        i = line[1:line.index('>')].split('/')[-1]
        ii = line[line.rindex('<'):line.rindex('>')].split('/')[-1]
        if "owl:SubClassOf" in line:# type
            if i in cons:
                i_type[i] = i_type.get(i,0)+1
            if ii in cons:
                i_sub[ii] = i_sub.get(ii,0)+1
        if "property#isRelatedTo" in line and "concept" in line: #related classes
            if i in cons:
                i_related[i] = i_related.get(i,0)+1
        if "owl:InstanceOf" in line:
            if ii in cons:
                i_ins[ii] = i_ins.get(ii,0)+1
    return i_type, i_sub, i_related, i_ins

if __name__=="__main__":
    top = get_top_concepts(CONCEPT_LIST)
    top_sub = get_sub_concepts(top, TAXONOMY)
    subs = []
    for v in top_sub.values():
        subs += v
    subs = set(subs)
    sub_sub = get_sub_concepts(subs, TAXONOMY)
    cons = [] 
    cons += top
    cons += list(subs)
    for v in sub_sub.values():
        cons += v
    print "cons:",cons
    print "cons num:",len(cons)
    label = label_stat(cons, CONCEPT_LIST)
    print "label:",label
    ttype, sub_class, related_class, instance = taxonomy_stat(cons, TAXONOMY)
    print "type:",ttype
    print "sub class:",sub_class
    print "related class:",related_class
    print "instance:",instance
    for i,v in instance.items():
        if i not in top and v < 40:
            cons.remove(i)
    print "cons num:",len(cons)
    prop = property_stat(cons, INSTANCE_INFOBOX)
    print "property"
    #print "property",prop
    with open('concept-statistics.txt','w') as f:
        f.write("level^^id^^label^^Super_Class_id^^Super_Class_label^^Type^^Sub_Classes^^Related_Classes^^Properties^^Instances\n")
        for i in top:
            if i in cons:
                f.write("%d^^%s^^%s^^%s^^%s^^%d^^%d^^%d^^%d^^%d**\n"%(1, i, label[i], "null", "Main topic classifications::;Root::;页面分类::;总分类", ttype.get(i,0), sub_class.get(i,0), related_class.get(i,0), prop.get(i,0), instance.get(i,0)))
                for j in top_sub[i]:
                    if j in cons:
                        f.write("%d^^%s^^%s^^%s^^%s^^%d^^%d^^%d^^%d^^%d**\n"%(2, j, label[j], i, label[i], ttype.get(j,0), sub_class.get(j,0), related_class.get(j,0), prop.get(j,0), instance.get(j,0)))
                        for k in sub_sub[j]:
                            if k in cons:
                                f.write("%d^^%s^^%s^^%s^^%s^^%d^^%d^^%d^^%d^^%d**\n"%(3, k, label[k], j, label[j], ttype.get(k,0), sub_class.get(k,0), related_class.get(k,0), prop.get(k,0), instance.get(k,0)))

