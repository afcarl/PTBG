#coding=utf8
__author__ = 'luocheng'

from collections import defaultdict
import os
from parseDefaultStrXml import parse
from parseDefaultStrXml import userVariance
from scipy.stats import linregress
from DocUtils import docsimi
def readTimeFitting(dupthreshold):
    # userRel: (user,doc) -> rel
    print dupthreshold
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
    doccontent = defaultdict(lambda:'')

    for f in os.listdir('../data/pages-content'):
        docid = f.replace('.txt','')
        content = open('../data/pages-content/'+f).read()
        doccontent[int(docid)] = content
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
        readdocs = []
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
                dcontent = doccontent[docid]
                duplicate = False

                for d in readdocs:
                    if docsimi(dcontent,d) > dupthreshold:
                        continue
                    else:
                        duplicate = True
                readdocs.append(dcontent)
                if dlength >100 and dheight >700 and duration > 5 and dlength < 30000 and duplicate == False:
                    userReadBehvOnDoc[user][0].append(duration)
                    userReadBehvOnDoc[user][1].append(dlength)
                    userReadBehvOnDoc[user][2].append(dheight)


    fout = open('../data/readingtime/threshold'+str(dupthreshold)+'.csv','w')

    fout.write('user,#samples,slope,intercept,r-value,p-value,stderr,slope,intercept,r-value,p-value,stderr\n')

    # raw
    raw = open('../data/raw-user-reading.csv','w')
    raw.write('user,dwelltime,dlength,dheight\n')

    for u in userReadBehvOnDoc:
        for i in range(0,len(userReadBehvOnDoc[u][0]),1):
            raw.write(','.join([str(item) for item in [u,userReadBehvOnDoc[u][0][i],
                                                        userReadBehvOnDoc[u][1][i],
                                                        userReadBehvOnDoc[u][2][i]]]))
            raw.write('\n')
    raw.close()

    check = open('../data/userbehavior-fine-grained.csv','w')

    for u in userReadBehvOnDoc:
        check.write(str(u)+'\n')
        check.write(','.join([str(item) for item in userReadBehvOnDoc[u][0] ])+'\n')
        check.write(','.join([str(item) for item in userReadBehvOnDoc[u][1] ])+'\n')
        check.write(','.join([str(item) for item in userReadBehvOnDoc[u][2] ])+'\n')
        fout.write(str(u)+','+str(len(userReadBehvOnDoc[u][0]))+',')
        slope1, intercept1, r1, p1, stderr1 = linregress(userReadBehvOnDoc[u][1],userReadBehvOnDoc[u][0])
        slope2, intercept2, r2, p2, stderr2 = linregress(userReadBehvOnDoc[u][2],userReadBehvOnDoc[u][0])
        import numpy as np
        length = np.array(userReadBehvOnDoc[u][1])
        height = np.array(userReadBehvOnDoc[u][2])

        fout.write(','.join([str(item) for item in [slope1, intercept1,r1,p1,stderr1,slope2,intercept2,r2,p2,stderr2]]))
        fout.write('\n')

    overall = [[],[],[]]
    for u in userReadBehvOnDoc:
        for i in range(0,len(userReadBehvOnDoc[u][0]),1):
            overall[0].append(userReadBehvOnDoc[u][0][i])
            overall[1].append(userReadBehvOnDoc[u][1][i])
            overall[2].append(userReadBehvOnDoc[u][2][i])

    slope1, intercept1, r1, p1, stderr1 = linregress(overall[1],overall[0])

    slope2, intercept2, r2, p2, stderr2 = linregress(overall[2],overall[0])

    # import matplotlib.pylab as plt
    #
    # fig, ax = plt.subplots()
    # ax.plot(overall[1],overall[0],'+')
    # ax.set_title('x = docment length; y = reading time')
    # plt.savefig('../data/figs/doclength.eps')
    #
    # fig, ax = plt.subplots()
    # ax.plot(overall[2],overall[0],'o')
    # ax.set_title('x = webpage length; y = reading time')
    # plt.savefig('../data/figs/webpagelength.eps')

    fout.write(','.join([str(item) for item in ['overall', len(overall[0]),slope1,intercept1,r1,p1,stderr1,slope2,intercept2,r2,p2,stderr2]]))

    summary = open('../data/readingtime/summmary.csv','a')
    summary.write(','.join([str(item) for item in [str(dupthreshold), len(overall[0]),slope1,intercept1,r1,p1,stderr1,slope2,intercept2,r2,p2,stderr2]])+"\n")
    fout.close()

for i in range(1,11,1):
    readTimeFitting(float(i)*0.10)