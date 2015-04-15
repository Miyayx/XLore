# -*- coding:utf-8 -*-

from pattern.en import pluralize, singularize

CONCEPT_LIST='/home/xlore/Xlore/etc/ttl/xlore.concept.list.ttl'
DBPEDIA_LIST='DBpediaclasses683.txt'
MATCH_OUTPUT='dbpedia_xlore_concept.dat'
NOTMATCH_OUTPUT='dbpedia_xlore_concept_notmatch.dat'

concepts = {}
zh_concepts = {}

def read_xlore_concepts(fn):
    print "Reading concept list..."    
    for line in open(CONCEPT_LIST):
        if line.startswith('<') and '@en' in line:
            i = line[0:line.index(' ')][1:-1]
            title = line[line.index('"')+1:line.rindex('"')]
            concepts[title.lower().strip()] = i
        if line.startswith('<') and '@zh' in line:
            i = line[0:line.index(' ')][1:-1]
            title = line[line.index('"')+1:line.rindex('"')]
            zh_concepts[i] = title

def read_dbpedia_concepts(output, fn):
    with open(output, 'w') as f:
        f_not = open(NOTMATCH_OUTPUT, 'w')
        ex_count = 0
        match_count = 0
        not_count = 0
        for line in open(fn):
            uri, label = line.strip('\n').split('\t')[:2]
            i = concepts.get(label.lower(), 0)
            if i:
                #print "Exact Match:",label
                ex_count += 1
                if i in zh_concepts:
                    f.write('%s\thttp://xlore.org/concept/%s\t%s@dbpedia\t%s@en@xlore\t%s@zh@xlore\n'%(uri,i, label, label, zh_concepts[i]))
                else:
                    f.write('%s\thttp://xlore.org/concept/%s\t%s@dbpedia\t%s@en@xlore\n'%(uri,i, label, label))
            else:
                n_label = pluralize(label)
                if label == 'activity':
                   print n_label
                   print concepts.get(n_label.lower())
                i = concepts.get(n_label.lower(), 0)
                if i:
                    #print "Plural Match",label
                    match_count += 1
                    if i in zh_concepts:
                        f.write('%s\thttp://xlore.org/concept/%s\t%s@dbpedia\t%s@en@xlore\t%s@zh@xlore\n'%(uri,i, label, n_label, zh_concepts[i]))
                    else:
                        f.write('%s\thttp://xlore.org/concept/%s\t%s@dbpedia\t%s@en@xlore\n'%(uri,i, label, label))
                else:
                    #print "Can't find:",label
                    not_count += 1
                    f.write('%s\t%s@dbpedia\n'%(uri, label))
                    f_not.write(line)
        f_not.close()
      
        print "ex_count:",ex_count
        print "match_count:",match_count
        print "not_count:",not_count

if __name__=="__main__":
    read_xlore_concepts(CONCEPT_LIST)
    read_dbpedia_concepts(MATCH_OUTPUT, DBPEDIA_LIST)
         
  
