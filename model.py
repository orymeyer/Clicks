from pymongo import MongoClient
import time,datetime,os



client = MongoClient(os.getenv("MONGO_URL"))
db = client.sandbox
cn = db.records



def createLink(bURL,id,userName):
    now = time.time()
    cn.insert({"time_stamp_created":now,"sURL":id,"bURL":bURL,"clicked":False,"userName":userName,"clicked_number":0,"clicks":{}})

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

def showStats(userName):
    kv = {}
    num = cn.find({"userName":userName}).count()
    data =  cn.find({"userName":userName},limit=10)
    for links in data:
        kv[links["bURL"]] = links["sURL"]
    return kv,num

def showLStats(id):
    res =  cn.find_one({"sURL":id})
    if res is None:
        return None
    res["_id"] = None
    #res["time_stamp_created"]= None
    return res

def removesURL(sUrl,userName):
    res = cn.find_one({"sURL":sUrl})
    if res["userName"]==userName:
        cn.remove(res)
        return True
    else:
        return False


