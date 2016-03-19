__author__ = 'luocheng'

import xml.etree.ElementTree as ET
from MetaDS import Topic, Session, Interaction, Result, Click, Examination


def parse():
    sessions = []
    tree = ET.parse('../data/modified_log_with_annotation.xml')
    root = tree.getroot()
    for sitem in root:

        # session
        session = Session()
        session.num = int(sitem.get('num'))
        session.starttime = float(sitem.get('starttime'))
        session.userid = int(sitem.get('userid'))

        # topic
        tnode = sitem[0]
        desc = tnode.find('desc').text
        init_query = tnode.find('init_query').text
        tnum = int(tnode.get('num'))
        topic = Topic(tnum, desc, init_query)
        session.topic = topic

        # multiple interactions
        for iitem in sitem[1:-1]:
            interaction = Interaction()
            interaction.num = int(iitem.get('num'))
            interaction.page_id = int(iitem.get('page_id'))
            interaction.starttime = float(iitem.get('starttime'))
            interaction.type = iitem.get('type')
            interaction.query = iitem[0].text

            # results
            for ritem in iitem.find('results'):
                result = Result(int(ritem.get('rank')),
                                ritem[0].text,
                                int(ritem[1].text),
                                ritem[2].text,
                                ritem[3].text)
                interaction.results.append(result)
            # clicks
            # Note that there are not necessarily clicks in an interaction.
            if iitem.find('clicked') != None:
                for citem in iitem.find('clicked'):
                    click = Click(float(citem.get('endtime')),
                                  int(citem.get('num')),
                                  float(citem.get('starttime')),
                                  int(citem[0].text),
                                  int(citem[1].text),
                                  int(citem[2].get('score')))
                    interaction.clicks.append(click)
            if iitem.find('examined')!= None:
                for eitem in iitem.find('examined'):
                    examination = Examination(int(eitem.get('duration')),
                                              float(eitem.get('endtime')),
                                              int(eitem.get('num')),
                                              float(eitem.get('starttime')),
                                              int(eitem.find('rank').text),
                                              int(eitem.find('docno').text)
                                              )
                    interaction.examinations.append(examination)
            interaction.query_satisfaction = int(iitem.find('query_satisfaction').get('score'))

            session.interactions.append(interaction)
        session.satisfaction= int(sitem.find('satisfaction').get('score'))
        sessions.append(session)

    return sessions
def calculateH(sessions):
    endtime = []
    for s in sessions:
        for i in s.interactions:
            if len(i.clicks) >=1:
                c = i.clicks[-1]
                if i.type == 'page':
                    endtime.pop()
                    endtime.append(c.endtime)
                else:
                    endtime.append(c.endtime)
    endtime.sort()
    return endtime[ int(len(endtime)/2) ]

def userVariance(sessions):
    from collections import defaultdict
    userSat = defaultdict(lambda:[])
    for s in sessions:
        userid = s.userid
        for i in s.interactions:
            q_sat = i.query_satisfaction
            if i.type == 'page':
                userSat[userid].pop()
                userSat[userid].append(q_sat)
            else:
                userSat[userid].append(q_sat)
    # user parameter -> user.mean, user.std
    userPara = defaultdict(lambda:[0.0,0.0])
    import numpy as np
    for u in userSat:
        userPara[u][0] = np.mean(np.array(userSat[u]))
        userPara[u][1] = np.std(np.array(userSat[u]))
    return userPara


class RelevanceService:
    def __init__(self):
        from collections import defaultdict
        self.userRelevance = defaultdict(lambda:0)
        for l in open('../data/relevance_user.tsv'):
            userid,docid,rel = l.strip().split('\t')
            self.userRelevance[(int(userid), int(docid))] = int(rel)
    def getUserRelevance(self,userid, docid):
        return self.userRelevance[(userid,docid)]

def TBG(clickArray,relevanceservice,userid,halftime):
    gain = 0.0
    import math
    for c in clickArray:
        docid  = c.docno
        rel = relevanceservice.getUserRelevance(userid,docid)
        starttime = c.starttime
        gain += rel * math.exp( (-1.0)*starttime*math.log(2)/halftime)
    return gain


def PTBG(clickArray,relevanceservice,userid,halftime,rate):

    gain = 0.0

    shrinkTime = 0.0

    import math
    for c in clickArray:
        docid = c.docno
        rel = relevanceservice.getUserRelevance(userid,docid)
        starttime = c.starttime
        gain += rel * math.exp( ( -1.0)* (starttime-shrinkTime)*math.log(2)/halftime)

        if rel <=2:
            shrinkTime += (c.endtime-c.starttime) * rate
    return gain

def calculateTBG(sessions):

    from collections import defaultdict

    half = calculateH(sessions)
    userPara = userVariance(sessions)
    rs = RelevanceService()

    user_tbg = defaultdict(lambda:[])
    user_ptbg = defaultdict(lambda:[])
    user_sat = defaultdict(lambda:[])

    for s in sessions:
        ptbg = []
        sat = []
        userid = s.userid
        multiClickArray = []

        for i in s.interactions:
            if i.type == 'page':
                for c in i.clicks:
                    multiClickArray[-1].append(c)
                sat.pop()
                sat.append(i.query_satisfaction)
            else:
                multiClickArray.append(i.clicks)
                sat.append(i.query_satisfaction)

        for iter in range(0, len(sat),1):
            if len(multiClickArray[iter]) >=1:
                user_tbg[userid].append( TBG(multiClickArray[iter],rs,userid,half))
                user_ptbg[userid].append( PTBG(multiClickArray[iter],rs,userid,half,0.1))
                user_sat[userid].append( (sat[iter]-userPara[userid][0])/userPara[userid][1])
    from scipy.stats.stats import pearsonr
    fout = open('../data/correlation-1.tsv','w')
    fout.write('user\t# of sessions\ttbg vs SAT\tp-value\tptbg vs SAT\tp-value\n')
    for u in user_sat:
        l=  len(user_tbg[u])
        r1,p1 = pearsonr( user_tbg[u],user_sat[u])
        r2,p2 = pearsonr( user_ptbg[u],user_sat[u])
        fout.write('\t'.join([str(item) for item in [u,l,r1,p1,r2,p2]])+'\n')
    fout.close()




if __name__ == "__main__":
    sessions = parse()
    half = calculateH(sessions)
    print half
    #
    # userPara = userVariance(sessions)
    # calculateTBG(sessions)



