#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import pagerank
import numpy as np

DIR="/home/xlore/Xlore/etc/ttl"
INSTANCE_REFERENCE="xlore.instance.reference.ttl"
s = (11721238,11721238)
A = np.zeros(s)
for line in open(os.path.join(DIR,INSTANCE_REFERENCE)):
    if not line.startswith('<'):
        continue
    a,_,b = line.split(" ")[:3]
    a = int(a[1:-1])
    b = int(b[1:-1])
    print a,b
    A[a-1,b-1] = 1

i = 1
for v in pagerank(A):
    print i,v
    

