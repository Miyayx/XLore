#!/usr/bin/python
#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import os

URL = "http://en.wikipedia.org/"
ROOT = "wiki/Category:Main_topic_classifications"

page = urllib2.urlopen(os.path.join(URL,ROOT)).read()
soup = BeautifulSoup(page)
top_sub = {}
sub_sub = {}
lis = soup.find_all(class_="CategoryTreeLabel")
for li in lis:
    print li.string
    page2 = urllib2.urlopen(os.path.join(URL,'wiki/Category:'+li.string)).read()
    soup2 = BeautifulSoup(page2)
    llis = soup2.find_all(class_="CategoryTreeLabel")
    for lli in llis:
        print lli.string
        top_sub[li.string] = lli.string
        try:
            page3 = urllib2.urlopen(os.path.join(URL,'wiki/Category:'+lli.string)).read()
        except:
            print "Error key:",lli.string
            continue
        soup3 = BeautifulSoup(page3)
        lllis = soup3.find_all(class_="CategoryTreeLabel")
        for llli in lllis:
            print llli.string
            sub_sub[lli.string] = llli.string
        
