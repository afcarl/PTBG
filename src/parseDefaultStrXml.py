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

if __name__ == "__main__":
    sessions = parse()
