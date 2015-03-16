#!/usr/bin/python

INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
PREFIX = 'http://www.baike.com/wiki/'
OUTPUT = 'hudong.icon.ttl'

import os
import urllib
from bs4 import BeautifulSoup

fo = open(OUTPUT,'w')
with open(INSTANCE_LIST) as f:
    line = f.readline()
    while line:
        if '@zh' in line:
            i = line[0:3]
            title = line[line.index('"')+1:line.rindex('"')]
            page = urllib.urlopen(os.path.join(PREFIX, title)).read()
            soup = BeautifulSoup(soup)
            imgurl = soup.find(class_='doc-img').find('img').src
            fo.write('%s property:hasIcon "%s"@baidu .\n')
            fo.flush()
fo.close()
            
