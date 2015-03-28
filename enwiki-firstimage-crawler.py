#!/usr/bin/python

INSTANCE_LIST='/home/xlore/Xlore/etc/ttl/xlore.instance.list.ttl'
PREFIX = 'http://en.wikipedia.org/wiki/'
OUTPUT = 'enwiki.icon.ttl'

import os
import urllib
from bs4 import BeautifulSoup

from subprocess import Popen,PIPE
import threading
import time

end = None 
if os.path.isfile(OUTPUT):
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
    imgdoc = soup.find(class_='infobox')
    if imgdoc:
        img = imgdoc.find('img')
        if img:
            imgurl = img['src']
            if not imgurl or len(imgurl) == 0:
                return
            print 'http:'+imgurl
            mutex.acquire()
            fo.write('%s property:hasIcon "http:%s"@enwiki .\n'%(i,imgurl))
            fo.flush()
            mutex.release()

with open(INSTANCE_LIST) as f:
    line = f.readline()
    while end:
       if end in line:
           line = f.readline()
           break
       line = f.readline()
    
    line = f.readline()
    while line:
        if '@en' in line:
            i = line[0:line.index(' ')]
            title = line[line.index('"')+1:line.rindex('"')]
            title = '_'.join(title.split())
            print i+' '+title
            t = threading.Thread(target=crawl, args=(i,title))
            t.start()
            t.join(7)
            if t.is_alive():
                print "timeout alive"
                line = f.readline()
                continue
        line = f.readline()
fo.close()
            
