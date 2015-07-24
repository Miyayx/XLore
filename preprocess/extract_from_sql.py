# -*- coding:utf-8 -*-
from hanziconv import HanziConv


def extract_langlinks(sql, fo):
    total = 0
    category = 0
    instance = 0
    template = 0

    o = open(fo, 'w')

    with open(sql) as f:
        for line in f:
            if line.startswith('INSERT'):
                line = line[line.index('('):]
                line = line.strip('\n').strip(';').strip(')').strip('(') #删除前后的（和）
                for tri in line.split('),('): #以),(分割，得出每个item
                    tri = tri.replace("'",'').replace("'",'') 
                    _id, lan, link = tri.split(',',2) #因为link里可能有逗号，要限制只分2次
                    if lan == 'zh':
                        total += 1
                        if link.startswith('Category:'):
                            category += 1
                        if link.startswith('Template:'):
                            template += 1
                            print _id, HanziConv.toSimplified(link).encode('utf-8')
                        link = link.replace('_', ' ')
                        o.write('%s\t%s\n'%(_id,HanziConv.toSimplified(link).encode('utf-8')))
    
    instance = total - category - template
    print "Total:%d, Category:%d, Instance:%d, Template:%d"%(total, category, instance, template)

NAMESPACE={
        '0':"",
        '10':"Template:",
        '14':"Category:"
        }

def extract_all_ids(sql, fo):
    
    total = 0
    category = 0
    instance = 0
    template = 0

    o = open(fo, 'w')
    with open(sql) as f:
        for line in f:
            if line.startswith('INSERT'):
                line = line[line.index('('):]
                line = line.strip(';').strip(')').strip('(') #删除前后的（和）
                for tri in line.split('),('): #以),(分割，得出每个item
                    total += 1
                    tri = tri.replace("'",'').replace("'",'')
                    _id, ns, title, _ = tri.split(',',3) #最后的_没用
                    if ns in NAMESPACE:
                        title = NAMESPACE[ns]+title
                        if ns == '10':
                            template += 1
                        if ns == '0':
                            instance += 1
                        if ns == '14':
                            category += 1
                        title = title.replace('_', ' ')
                        o.write('%s\t%s\n'%(title, _id))
                        o.flush()
    o.close()
    
    print "Total:%d, Category:%d, Instance:%d, Template:%d"%(total, category, instance, template)

def find_template_cl(fid, fzh, fo):
    d = {}
    for line in open(fid):
        if line.startswith('Template:'):
            en, _id = line.strip('\n').split('\t')
            d[_id] = en
    o = open(fo, 'w')
    for line in open(fzh):
        print line
        _id, zh = line.strip('\n').split('\t')
        if zh.startswith('Template:') and _id in d:
            o.write('%s\t%s\n'%(d[_id], zh))
            o.flush()
    o.close()

if __name__ == '__main__':
    extract_all_ids('zhwiki-20150703-page.sql', 'zhwiki-id.dat')
    #extract_langlinks('enwiki-20150702-langlinks-zh.sql', 'enwiki.id.zh')
    #find_template_cl('enwiki-id.dat','enwiki.id.zh','template.cl')


