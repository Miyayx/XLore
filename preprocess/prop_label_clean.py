#!/usr/bin/python
#-*- coding:utf-8 -*-

import codecs
OLD="/home/xlore/Xlore/etc/taxonomy/wikis/hudong-dump-20140808.dat"
NEW="/home/xlore/Xlore/etc/taxonomy/wikis/hudong-dump-20150702.dat"
OLD_LABEL="/home/xlore/Xlore/etc/taxonomy/wikis/hudong-property-label-20141212.dat"
NEW_LABEL="/home/xlore/Xlore/etc/taxonomy/wikis/hudong-property-label-20150416.dat"

def polish_label(label):
    return label.decode('utf-8').replace('\t','').strip(',').lstrip(';').strip(u'：') \
               .strip(':').strip(': -').strip(u'；').strip(u'【').strip(u'】') \
               .strip(u'`').strip(u'，').lstrip('*').replace(' ','') \
               .encode('utf-8')

f = codecs.open(NEW,'w')
old_labels = set()
new_labels = set()

count = 0
for line in open(OLD):
    if line.startswith('Infoboxes:'):
        text = line.strip('\n').split(': ',1)[1]
        infos = []
        for b in text.split('::;'):
            k,v = b.split('::=')
            old_labels.add(k)
            nk = polish_label(k)
            if not nk == k:
                print line
                print nk,k
                count += 1
            new_labels.add(nk)
            infos.append((nk,v))
        infs = ['::='.join(i) for i in infos]
        line = "Infoboxes: %s\n"%('::;'.join(infs))
    f.write(line)
    f.flush()
f.close()

print "modify:",count

print "Origin Number:",len(old_labels)
with open(OLD_LABEL, 'w') as f:
    for l in sorted(old_labels):
        f.write(l+"\n")

print "New Number:",len(new_labels)
with codecs.open(NEW_LABEL, 'w','utf-8') as f:
    for l in sorted(new_labels):
        f.write(l+"\n")
        
