#/usr/bin/python
# -*- coding=utf-8 -*-

MENTION_FILES = (
'/home/xlore/disk2/raw.wiki/enwiki-linkmention.dat',
'/home/xlore/disk2/raw.wiki/enwiki-infobox-redirect.dat'
)

INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
SEPERATOR = "\t\t"
OUTPUT = "/home/xlore/disk2/raw.wiki/mention2entity"

d = {}
instances = {}

for line in open(INSTANCE_LIST):
    if line.startswith('<'):
        i = line[0:line.index(' ')][1:-1]
        title = line[line.index('"')+1:line.rindex('"')]
        instances[title] = i

for fn in MENTION_FILES:
    for line in open(fn):
        title, mention = line.strip().split(SEPERATOR)
        i = instances[title]
        ids = d.get(mention, {})
        ids[i] = ids.get(i,0)+1
        d[mention] = ids

with open(OUTPUT, 'w') as f:
    for k, v in d.iteritems():
        for k1, v1 in sorted(d, key = lambda x:x[1]):
            f.write("%s::;%s::;%d"%(k, k1, v1))
    
