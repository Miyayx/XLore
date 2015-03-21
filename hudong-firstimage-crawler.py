#!/usr/bin/python

INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
PREFIX = 'http://www.baike.com/wiki/'
OUTPUT = 'hudong.icon.ttl'

import os
import urllib
from bs4 import BeautifulSoup

from subprocess import Popen,PIPE
import threading
import time

p = Popen(['tail','-n','1',OUTPUT], stdout=PIPE)
o,e = p.communicate()
end = o[0:o.index(' ')]
print "end-->"+end

fo = open(OUTPUT,'a')
mutex = threading.Lock()

def crawl(i, title):
    global mutex

    page = urllib.urlopen(os.path.join(PREFIX, title))
    soup = BeautifulSoup(page)
    #print soup.find(class_='doc-img').find('img')
    imgdoc = soup.find(class_='doc-img')
    if imgdoc:
        imgurl = imgdoc.find('img')['src']
        if not imgurl or len(imgurl) == 0:
            return
        print imgurl
        mutex.acquire()
        fo.write('%s property:hasIcon "%s"@hudong .\n'%(i,imgurl))
        fo.flush()
        mutex.release()

with open(INSTANCE_LIST) as f:
    line = f.readline()
    while True:
       if end in line:
           line = f.readline()
           break
       line = f.readline()
    
    line = f.readline()
    while line:
        if '@zh' in line:
            i = line[0:line.index(' ')]
            title = line[line.index('"')+1:line.rindex('"')]
            print i+''+title
            t = threading.Thread(target=crawl, args=(i,title))
            t.start()
            t.join(8)
            if t.is_alive():
                print "timeout alive"
                line = f.readline()
                continue
        line = f.readline()
fo.close()
            
