__author__ = 'luocheng'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def extractFromDB():
    import sqlite3
    db = sqlite3.connect('../data/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM anno_searchresult')
    items = cursor.fetchall()
    fout = open('../data/allsearchresult.tsv','w')
    for item in items:
        fout.write(str(item[0])+'\t'+item[1].decode('utf8').encode('utf8')+'\t'+item[2]+'\n')
    fout.close()
    cursor.execute('SELECT * from anno_annotation')
    fout = open('../data/userannotation.tsv','w')
    for item in cursor.fetchall():
        fout.write('\t'.join([str(s) for s in [item[1],item[2],item[3],item[4],item[6]]]))
        fout.write('\n')
    db.close()

def getTwoKindRelevance():
    local2global = dict()
    for l in open('../data/allsearchresult.tsv'):
        globalid,query,localid = l.strip().split('\t')
        local2global[(query,localid)] = globalid
    fout = open('../data/relevance_user.tsv','w')
    for l in open('../data/userannotation.tsv'):
        userid,_,query,localid,rel = l.strip().split("\t")
        fout.write(userid+'\t'+local2global[(query,localid)]+'\t'+rel+'\n')
    fout.close()

getTwoKindRelevance()