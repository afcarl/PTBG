__author__ = 'luocheng'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def extractUrls():
    import sqlite3
    db = sqlite3.connect('../data/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM anno_searchresult')
    items = cursor.fetchall()
    fout = open('../data/url.tsv','w')

    for item in items:
        globalid = str(item[0])
        q = item[1]
        rank = int(item[3])
        content = item[4]
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content)
        url= soup.find('a').get('href')
        if rank <= 5:
            print globalid
            fout.write(globalid+'\t'+str(rank)+'\t'+q+'\t'+url+'\n')

    fout.close()

extractUrls()