#/usr/bin/python
# -*- coding=utf-8 -*-

REDIRECT = "/home/xlore/disk2/raw.wiki/enwiki-infobox-redirect.dat"

MENTION_FILES = (
'/home/xlore/disk2/raw.wiki/enwiki-linkmention.dat',
'/home/xlore/disk2/raw.wiki/enwiki-infobox-redirect.dat'
)

#对于每个wiki，把它的title看做mention，计数为1
#主要是要把baidu，hudong的数据利用起来
TITLE_FILES = (
'/home/xlore/Xlore/etc/taxonomy/raw.wiki/hudong-instanceList-all.dat',
'/home/xlore/Xlore/etc/taxonomy/raw.wiki/baidu-instanceList-all.dat',
'/home/xlore/Xlore/etc/taxonomy/raw.wiki/enwiki-instanceList-all.dat',
'/home/xlore/Xlore/etc/taxonomy/raw.wiki/zhwiki-instanceList-all.dat',
)

INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
SEPERATOR = "\t\t"
OUTPUT = "/home/xlore/disk2/raw.wiki/mention2entity"

d = {}
instances = {}

print "Reading instance list..."    
for line in open(INSTANCE_LIST):
    if line.startswith('<') and 'rdfs:label' in line:
        i = line[0:line.index(' ')][1:-1]
        title = line[line.index('"')+1:line.rindex('"')]
        instances[title.lower().strip()] = i
print "Instances:",len(instances)

print "Adding redirect instances..."    
for line in open(REDIRECT):
    re, title = line.strip('\n').split(SEPERATOR)
    title = title.split('#',1)[0]
    re = re.lower().strip()
    title = title.lower().strip()
    if re in instances and not title in instances:
        instances[title] = instances[re]
    elif not re in instances and title in instances:
        instances[re] = instances[title]
print "Instances:",len(instances)

count = 0

for fn in MENTION_FILES:
    for line in open(fn):
        try:
            title, mention = line.strip('\n').split(SEPERATOR)
        except Exception,e:
            print e
            print line
            continue
        if len(mention.strip()) == 0:
            print "mention:",mention
            print line
            print count
            count += 1
            continue
        if '#' in title:
            title = title.split('#',1)[0]
        if ':' in title:
            title = title.split(':')[-1]
        i = instances.get(title.lower().strip(), 0)
        if not i:
            print "Don't have title:",title
            print line
            print count
            count += 1
            continue
        ids = d.get(mention, {})
        ids[i] = ids.get(i,0)+1
        d[mention] = ids

for fn in TITLE_FILES:
    for line in open(fn):
        title = line.strip('\n')
        i = instances.get(title.lower().strip(), 0)
        if not i:
            continue
        ids = d.get(title, {})
        ids[i] = ids.get(i,0)+1
        d[title] = ids

with open(OUTPUT, 'w') as f:
    for k, v in d.iteritems():
        for k1, v1 in sorted(v.items(), key = lambda x:x[1]):
            f.write("%s::;%s::;%d\n"%(k, k1, v1))
    
