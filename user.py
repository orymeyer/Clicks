from pymongo import MongoClient
import os


client = MongoClient(os.getenv("MONGO_URL"))
db = client.sandbox
ucn = db.users

def returnUser(uName):
    if ucn.find_one({"userName":uName}) is not None:
        return True #userExists
    else:
        return False #user does not exist

def registerUser(uName,email,pass_hash):

    ucn.insert({"userName":uName,"email":email,"pass":pass_hash})


def returnPHash(user):
    res = ucn.find_one({"userName":user})
    if res is not None:
        return res["pass"] #matches
    else:
        return False #no match

