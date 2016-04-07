#coding=utf8
__author__ = 'luocheng'

import  jieba





def docsimi(doc1, doc2):
    l1 = ' '.join(jieba.cut(doc1,cut_all=False)).split(' ')
    l2 = ' '.join(jieba.cut(doc2,cut_all=False)).split(' ')

    from collections import defaultdict
    d1 = defaultdict(lambda:0)
    d2 = defaultdict(lambda:0)
    for item in l1:
        d1[item] +=1
    for item in l2:
        d2[item] +=1
    jiaoji = 0
    bingji = 0

    kset =  set()
    for item in d1:
        kset.add(item)
    for item in d2:
        kset.add(item)

    for k in kset:
        jiaoji += min(d1[k],d2[k])
        bingji += max(d1[k],d2[k])
    return 1- float(jiaoji)/float(bingji)




