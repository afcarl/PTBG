#coding=utf8

__author__ = 'luocheng'


from bs4 import BeautifulSoup
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


count = 0
for f in os.listdir('../data/pages'):
    count +=1
    print count
    soup = BeautifulSoup(open('../data/pages/'+f).read())

    fout = open('../data/pages-modify/'+f,'w')
    fout.write(soup.prettify().encode('utf8'))
    fout.close()


from extract_content import ContentExtractor

import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

count = 0
for f in os.listdir('../data/pages-modify'):
    print count,5400

    count +=1
    ext = ContentExtractor()
    body,title = ext.analyse(open('../data/pages-modify/'+f).read())

    fout = open('../data/pages-content/'+f.replace('.html','.txt'),'w')
    fout.write(title+'\n')
    fout.write(body+'\n')
    fout.close()