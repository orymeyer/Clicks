from pymongo import MongoClient
import time,datetime,os

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.sandbox
cn = db.records



def createLink(bURL,id):
    now = time.time()
    cn.insert({"time_stamp_created":now,"sURL":id,"bURL":bURL,"clicked":False,"clicked_number":0,"clicks":{}})

'''
def recordLinkClick(id,ip,ua,ref):
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    res = cn.find_one({"lid":id})
    res["useragent"] = ua
    res["ref"]= ref
    res["clicked"]=True
    res["clicked_number"]+=1
    res["clicks"][str(now)]=ip
    cn.save(res)
'''


def recordLinkClick(sURL,ip,ua,ref):
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    res = cn.find_one({"sURL":sURL})
    res["clicked"]=True
    res["clicked_number"]+=1
    res["clicks"][str(now)]={"ip":ip,"ua":ua,"ref":ref}
    cn.save(res)
    return res["bURL"]


def update(id,details):
    res = cn.find_one({"sURL":id})
    if res.has_key('details'):
        pass
    else:
        res["details"]=details
        cn.save(res)

def showLinkStats(id):
    return cn.find_one({"sURL":id})
