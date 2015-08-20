from pymongo import MongoClient
import time,datetime,os

client = MongoClient('mongodb://207.46.227.159:27017/')
db = client.sandbox
cn = db.records



def createTrap(id):
    now = time.time()
    cn.insert({"time_stamp_created":now,"lid":id,"clicked":False,"clicked_number":0,"clicks":{}})

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


def recordLinkClick(id,ip,ua,ref):
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    res = cn.find_one({"lid":id})
    res["clicked"]=True
    res["clicked_number"]+=1
    res["clicks"][str(now)]={"ip":ip,"ua":ua,"ref":ref}
    cn.save(res)


def update(id,details):
    res = cn.find_one({"lid":id})
    if res.has_key('details'):
        pass
    else:
        res["details"]=details
        cn.save(res)

def showLinkStats(id):
    return cn.find_one({"lid":id})
