#!/usr/bin/python
#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import os

URL = "http://en.wikipedia.org/"
ROOT = "wiki/Category:Main_topic_classifications"

fliter_str = ['wikipedia', 'wikiprojects', 'lists', 'mediawiki', 'template', 'user', 'portal', 'categories', 'articles', 'pages', 'by'] 
def is_category(string):
    for f in fliter_str:
        if f in string:
            return False
    return True

def main():

    page = urllib2.urlopen(os.path.join(URL,ROOT)).read()
    soup = BeautifulSoup(page)
    top_sub = {}
    sub_sub = {}
    lis = soup.find_all(class_="CategoryTreeLabel")
    for li in lis[:]:
        print "0 "+li.string
        if not is_category(li.string):
            continue
        
        try:
            page2 = urllib2.urlopen(os.path.join(URL,'wiki/Category:'+"_".join(li.string.split()))).read()
        except:
            print "Error key:",li.string
            continue
        soup2 = BeautifulSoup(page2)
        llis = soup2.find(id="mw-subcategories").find_all(class_="CategoryTreeLabel")
        for lli in llis[:]:
            print "1 "+lli.string
            if not is_category(lli.string):
                continue
            top_sub[li.string.encode('utf-8')] = top_sub.get(li.string.encode('utf-8'),[])+[lli.string.encode('utf-8')]
            try:
                page3 = urllib2.urlopen(os.path.join(URL,'wiki/Category:'+'_'.join(lli.string.split()))).read()
            except:
                print "Error key:",lli.string
                continue
            soup3 = BeautifulSoup(page3)
            lllis = soup3.find_all(class_="CategoryTreeLabel")
            for llli in lllis:
                print "2 "+llli.string
                if not is_category(llli.string):
                    continue
                sub_sub[lli.string.encode('utf-8')] = sub_sub.get(lli.string.encode('utf-8'),[])+[llli.string.encode('utf-8')]

    return top_sub, sub_sub

if __name__=="__main__":
    main()
        
