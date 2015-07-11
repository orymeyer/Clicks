from pymongo import MongoClient
import time,datetime,os

client = MongoClient(os.getenv("MONGO_URL"))
db = client.sandbox
cn = db.records



def createTrap(id):
    now = time.time()
    cn.insert({"time_stamp_created":now,"lid":id,"clicked":False,"clicked_number":0,"clicks":{}})

def recordLinkClick(id,ip):
    ts = time.time()
    now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    res = cn.find_one({"lid":id})
    res["clicked"]=True
    res["clicked_number"]+=1
    res["clicks"][str(now)]=ip
    cn.save(res)

def update(id,details)
    res = cn.find_one({"lid":id})
    if res.has_key('details'):
        pass
    else:
        res["details"]=details
        cn.save(res)

def showLinkStats(id):
    return cn.find_one({"lid":id})

