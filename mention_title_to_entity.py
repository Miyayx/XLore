#/usr/bin/python
#-*-coding=utf8-*-

"""
利用已有的mention与对应instance label的统计信息，生成新版本的mention与instance id的关系,结果导入数据库
"""

INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
MENTION_TITLE_COUNT='/home/xlore/disk2/raw.wiki/Mention_Title_Count.dat'
MENTION_ENTITY_COUNT='/home/xlore/disk2/raw.wiki/Mention_Entity_Count.dat'

instances = {}

for line in open(INSTANCE_LIST):
    if line.startswith('<') and "rdfs:label" in line:
        i = line[0:line.index(' ')][1:-1]
        title = line[line.index('"')+1:line.rindex('"')]
        instances[title.lower()] = i

with open(MENTION_ENTITY_COUNT, 'w') as f:
    for line in open(MENTION_TITLE_COUNT):
        m, t, c = line.strip('\n').split('::;')
        t = t.strip()
        try:
            f.write("%s::;%s::;%s\n"%(m, instances[t.lower()], c))
            f.flush()
        except Exception,e:
            print t 
            continue

