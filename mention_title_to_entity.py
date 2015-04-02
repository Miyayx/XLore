
#/usr/bin/python
# -*- coding=utf-8 -*-

"""
利用已有的mention与对应instance label的统计信息，生成新版本的mention与instance id的关系,结果导入数据库
"""

INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
MENTION_TITLE_COUNT=''
MENTION_ENTITY_COUNT='/home/xlore/disk2/raw.wiki/Mention_Entity_Count.dat'

instances = {}

for line in open(INSTANCE_LIST):
    if line.startswith('<'):
        i = line[0:line.index(' ')][1:-1]
        title = line[line.index('"')+1:line.rindex('"')]
        instances[title] = i

with open(MENTION_ENTITY_COUNT, 'w') as f:
    for line in open(MENTION_TITLE_COUNT):
        m, t, c = line.strip('\n').split('::;')
        f.write("%s::;%s::;%s\n"%(m, instances[t], c))
        f.flush()

