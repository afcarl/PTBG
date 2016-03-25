__author__ = 'luocheng'


from parseDefaultStrXml import parse
from parseDefaultStrXml import userVariance
from collections import defaultdict
from ReadingTimeFit import linearfit
import os
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def calculateUserReading():

    # userRel: (user,doc) -> rel
    userRel = defaultdict(lambda:-1)

    # objectRel: (query, doc) -> rel
    objectRel = defaultdict(lambda:-1)

    for l in open('../data/relevance_user.tsv'):
        user, docid,rel =l.strip().split('\t')
        userRel[ ( int(user), int(docid))] = int(rel)
    for l in open('../data/relevance_9_all.tsv'):
        query,docid, rel = l.strip().split('\t')
        objectRel[ ( query, int(docid))] = int(rel)


    doclength = defaultdict(lambda:-1)
    imagelength = defaultdict(lambda:-1)
    for f in os.listdir('../data/pages-content'):
        docid = f.replace('.txt','')
        doclength[int(docid)] = len(open('../data/pages-content/'+f).read())

    for f in os.listdir('../data/screenshots'):
        docid = f.replace('.png','')
        from PIL import Image
        im = Image.open('../data/screenshots/'+f)
        width, height = im.size
        imagelength[int(docid)] = height



    sessions = parse()
    uservariance = userVariance(sessions)

    #user reading behavior   user -> dwell time, doc length, picture length
    userReadBehvOnDoc = defaultdict(lambda:[[],[],[]])

    for s in sessions:
        for i in s.interactions:
            for c in i.clicks:
                duration = c.endtime - c.starttime
                docid = int(c.docno)
                user = int(s.userid)
                rel = userRel[(user,docid)]
                if rel < 3:
                    continue
                dlength = doclength[docid]
                dheight = imagelength[docid]

                if dlength >0 and dheight >0:
                    userReadBehvOnDoc[user][0].append(duration)
                    userReadBehvOnDoc[user][1].append(dlength)
                    userReadBehvOnDoc[user][2].append(dheight)

    fout = open('../data/readingBehaviorFit34.csv','w')
    fout.write('user,#samples,dlength-slope,dlength-intercept,dlength-r,length.mean,length.std,dheight-slope,dheight-intercept,dheight-r,height.mean,height.std\n')

    check = open('../data/userbehavior.csv','w')

    for u in userReadBehvOnDoc:
        check.write(str(u)+'\n')
        check.write(','.join([str(item) for item in userReadBehvOnDoc[u][0] ])+'\n')
        check.write(','.join([str(item) for item in userReadBehvOnDoc[u][1] ])+'\n')
        check.write(','.join([str(item) for item in userReadBehvOnDoc[u][2] ])+'\n')
        fout.write(str(u)+','+str(len(userReadBehvOnDoc[u][0]))+',')
        linepara1, r1 = linearfit(userReadBehvOnDoc[u][1],userReadBehvOnDoc[u][0])
        linepara2, r2 = linearfit(userReadBehvOnDoc[u][2],userReadBehvOnDoc[u][0])
        import numpy as np
        length = np.array(userReadBehvOnDoc[u][1])
        height = np.array(userReadBehvOnDoc[u][2])

        fout.write(','.join([str(item) for item in [linepara1[0],linepara1[1],r1[0],length.mean(),length.std(),linepara2[0],linepara2[1],r2[0],height.mean(),height.std()]]))
        fout.write('\n')

    overall = [[],[],[]]
    for u in userReadBehvOnDoc:
        for i in range(0,len(userReadBehvOnDoc[u][0]),1):
            overall[0].append(userReadBehvOnDoc[u][0][i])
            overall[1].append(userReadBehvOnDoc[u][1][i])
            overall[2].append(userReadBehvOnDoc[u][2][i])
    linepara1, r1 = linearfit(overall[1],overall[0])
    linepara2, r2 = linearfit(overall[2],overall[0])
    fout.write(','.join([str(item) for item in ['overall', '#',linepara1[0],linepara1[1],r1[0],'#','#',linepara2[0],linepara2[1],r2[0]]]))

    fout.close()

def TBG():
    objectRel = defaultdict(lambda:-1)

    doclength = defaultdict(lambda:-1)
    for f in os.listdir('../data/pages-content'):
        docid = f.replace('.txt','')
        doclength[int(docid)] = len(open('../data/pages-content/'+f).read())

    for l in open('../data/relevance_9_all.tsv'):
        query,docid, rel = l.strip().split('\t')
        objectRel[int(docid)] = int(rel)

    query2tbg = {}
    query2ptbg = {}
    sessions = parse()


    for s in sessions:
        for i in s.interactions:
            q = i.query
            if q in query2tbg:
                continue
            else:
                results = []
                for r in i.results[0:5]:
                    results.append(r)
                tbg = 0
                tbgcumtime = 0
                ptbg = 0
                ptbgcumtime = 0
                valid = True
                for r in results:
                    docid = int(r.id)
                    rel = objectRel[docid]
                    if rel == -1:
                        valid = False
                    else:
                        tbg = rel*math.exp(tbgcumtime*math.log(2)/229.842)
                        ptbg = rel*math.exp(ptbgcumtime*math.log(2)/229.842)
                        dlength =doclength[docid]
                        if dlength == -1:
                            valid = False
                        else:
                            simutime = 0.00103367*dlength+42.95761547
                            if rel>=3:
                                p_click = 0.64
                            else:
                                p_click = 0.39
                            tbgcumtime+=simutime*p_click
                            if rel<3:
                                ptbgcumtime+=simutime*0.8*p_click
                            else:
                                ptbgcumtime+=simutime*p_click
                if valid==True:
                    query2tbg[q] = tbg
                    query2ptbg[q] = ptbg

    user2tbg = defaultdict(lambda:[])
    user2ptbg = defaultdict(lambda:[])

    user2sat = defaultdict(lambda:[])
    user2queries = defaultdict(lambda:set())


    for s in sessions:
        u = s.userid
        for i in s.interactions:
            q = i.query
            if q not in user2queries[u]:
                if q in query2tbg:
                    tbg = query2tbg[q]
                    ptbg = query2ptbg[q]
                    sat = i.query_satisfaction
                    user2tbg[u].append(tbg)
                    user2ptbg[u].append(ptbg)
                    user2sat[u].append(sat)
                    user2queries[u].add(q)
    import scipy.stats as stats
    fout = open('../data/tbg_ptbg_kendall_tau.csv','w')
    fout.write('user, # samples ,tbg v.s. sat(raw), p-value, ptbg v.s. sat(raw),p-value\n')
    for u in user2tbg:
        k1,p1 = stats.kendalltau(user2sat[u],user2tbg[u])
        k2,p2 = stats.kendalltau(user2sat[u],user2ptbg[u])
        fout.write(','.join([str(item) for item in [u,len(user2sat[u]),k1,p1,k2,p2]])+'\n')
    fout.close()

    fout = open('../data/tbg_ptbg_pearsonr.csv','w')
    fout.write('user, # samples ,tbg v.s. sat(raw), p-value, ptbg v.s. sat(raw),p-value\n')
    for u in user2tbg:
        k1,p1 = stats.pearsonr(user2sat[u],user2tbg[u])
        k2,p2 = stats.pearsonr(user2sat[u],user2ptbg[u])
        fout.write(','.join([str(item) for item in [u,len(user2sat[u]),k1,p1,k2,p2]])+'\n')
    fout.close()



if __name__=="__main__":
    TBG()