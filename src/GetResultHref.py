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

    alreadyin = set()
    for item in items:
        globalid = str(item[0])
        q = item[1]
        rank = int(item[3])
        content = item[4]
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content)
        url= soup.find('a').get('href')
        if rank <= 5:
            fout.write(globalid+'\t'+str(rank)+'\t'+q+'\t'+url+'\n')
            alreadyin.add(globalid)



    local2global = dict()
    for l in open('../data/allsearchresult.tsv'):
        globalid,query,localid = l.strip().split('\t')
        local2global[(query,localid)] = globalid


    cursor.execute("SELECT * FROM anno_annotation")
    items = cursor.fetchall()
    for item in items:
        query = str(item[3])
        localid = str(item[4])
        try:
            globalid = local2global[(query,localid)]
            rank = 0
            url = item[5]
            if globalid in alreadyin:
                print 'already in !', globalid
            else:
                alreadyin.add(globalid)
                fout.write(globalid+'\t'+str(rank)+'\t'+query+'\t'+url+'\n')
        except:
            print query,localid


    fout.close()
    cursor.close()

extractUrls()