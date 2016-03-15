__author__ = 'luocheng'


class Topic:
    def __init__(self,number,desc,initq):
        self.number = number
        self.desc = desc
        self.init_query = initq

class Result:
    def __init__(self,rank,url,id,title,snippet):
        self.rank = int(rank)
        self.url = url
        self.id = int(id)
        self.title = title
        self.snippet = snippet

class Click:
    def __init__(self,endtime,num,starttime,rank,docno,annotation):
        self.endtime = float(endtime)
        self.num= int(num)
        self.starttime = float(starttime)
        self.rank = int(rank)
        self.docno = int(docno)
        self.annoation = annotation

class Examination:
    def __init__(self,duration,endtime,num,starttime,rank,docno):
        self.duration = int(duration)
        self.endtime = float(endtime)
        self.num= int(num)
        self.starttime = float(starttime)
        self.rank = int(rank)
        self.docno = int(docno)




class Interaction:
    def __init__(self):
        self.num = None
        self.page_id = None
        self.starttime = None
        self.type = None
        self.query = None
        self.results = []
        self.clicks = []
        self.examinations = []
        self.query_satisfaction = None


class Session:
    def __init__(self):
        self.num = None
        self.starttime = None
        self.userid = None
        self.topic = None
        self.interactions = []
        self.satisfaction = None


