#!/usr/bin/python
#-*- coding:utf-8 -*-

class FirstImage:

    def __init__(self, i, o, ttl):
        self.input = i
        self.output = o
        self.ttl = ttl

    def extract(self):
        pass

    def generate_ttl(self,images):
        pass

    def get_images(self):
        return dict((line.strip('\n').split('\t')) for line in open(self.output))

    def run(self):
        self.extract()
        self.generate_ttl(self.get_images())


    


    
