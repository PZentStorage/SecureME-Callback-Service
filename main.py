from fastapi import FastAPI, Request
import requests
import time
import hashlib, base64
import json
import os
from dotenv import load_dotenv
import pymongo
import urllib.request
import webbrowser
from pydantic import BaseModel
import pickle
import redis
from datetime import datetime
load_dotenv()


app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
redis_conn = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
# Connection Mongo Database
client = pymongo.MongoClient(os.getenv('MONGO_URL'))
# mydb = client["securemedb-dev"]
mydb = client["iot-centralization-db"]
default_path_api = "/api/v1"

app = FastAPI()

def update_or_create_user_permission(userid, usertoken, fet_id):
    print(userid, usertoken, fet_id)
    # try:
    # column = mydb["fetcher_authenticate"]
    column = mydb["lifesmart_authentication"]
    
    query = column.find({
    "$and" : [{
                "app_key" : { "$eq" : os.getenv('APPKEY') },
            },
            {
                "app_token" : { "$eq" : os.getenv('APPTOKEN') },
            },
            {
                "fetcher_id" : { "$eq" : int(fet_id)}
            }
            ]
    })[0:1]
    
    for item in query:
        
        ids = item['_id']
        res = column.update_one({'_id':ids}, {"$set": { "user_id": userid, "user_token": usertoken }}, upsert=False)
        print(res)
        make_key = f"{fet_id}+{os.getenv('APPKEY')}"
        datas = {"user_id": userid, "user_token": usertoken}
        redis_conn.set(make_key, pickle.dumps(datas))
    return 200

    # except Exception as e:
    #     return e  


@app.get("/callback")
async def root(req: Request):
    userid = req.query_params['userid']
    usertoken = req.query_params['usertoken']
    fet_id = req.query_params['id']
    # print(userid, usertoken)
    print(req.query_params)
    
    make_key = f"{int(fet_id)}+{os.getenv('APPKEY')}"
    datas = {"user_id": userid, "user_token": usertoken}
    res = redis_conn.set(make_key, pickle.dumps(datas))
    print(res)
    dict_bytes = redis_conn.get(make_key)
    # print(dict_bytes)
    my_dict = pickle.loads(dict_bytes)
    print(my_dict)
    update_or_create_user_permission(my_dict['user_id'], my_dict['user_token'], fet_id)

    return {"message": "Successful"}


