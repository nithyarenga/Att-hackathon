from bottle import route, run
from bottle import request, response
from bottle import post, get, put, delete
from pymongo import MongoClient
from json import dumps, loads
from bson import json_util
from m2x.client import M2XClient
from datetime import datetime
from requests.exceptions import HTTPError
import StringIO
import send_tweet as tweet
import datetime

client = MongoClient()
db = client.lighthouse

client = M2XClient(key="dbbbb260442d2411fb43e2f1917a8d88")


@get('/hello')
def hello():
    return "Hello World!"

@get('/m2x_trigger')
def m2x_trigger():
    # Find the correct device if it exists, if not create it.
    try:
        device = [d for d in client.devices(q="m2x-att") if d.name == "m2x-att"][0]
    except IndexError:
        device = client.create_device(name="m2x-att",
                                      visibility="private")

    # Get the stream if it exists, if not create the stream.
    stream = device.stream("counter")
    postime = datetime.now()
    stream.add_value(db.put_counter.count(), postime)

@post('/m2x_trigger')
def m2x_trigger():
    value = request.body.read()
    v = loads(value)
    tweet.create_tweet(v["custom_data"])

@get('/alerts')
#color
#list of strings
def returnarray():

    if db.alerts.count() == 0:
        rv = { "color": "blue", "text": "Tornados are expected in dallas downtown at 10:30pm" }
        response.content_type = 'application/json'
        return dumps(rv)
    else:
        query = db.alerts.find().sort('date',-1).limit(1)

        for doc in query:
            return json_util.dumps(doc)


@get('/shelter')
#name, address
def returnarray():
    # add logic if no matching results

    if db.shelter_dir.count() == 0:
        rv = { "text": ["welcome-home", "111 legendary drive", "will take 15 mins to reach by walk"]}
        response.content_type = 'application/json'
        return dumps(rv)
    else:
        # How to sort the database? based on location?
        query = db.shelter_dir.find({}).sort("distance",1).limit(1)
        for doc in query:
            db.put_counter.insert({"name":doc["name"],"aid":request.query.alexa, "endpoint":"shelter"})
            final = {"text" : [doc["name"], doc["address"], "is " + str(int(doc["distance"]))+" minutes away"], "women": False}
            return final

@get('/emergency')
#name
#address
def returnarray():
    if db.emergency_dir.count() == 0:
        rv = { "text": ["welcome-home", "111 legendary drive" , "will take 2 min to reach by run"]}
        response.content_type = 'application/json'
        return dumps(rv)
    else:
        # How to sort the database? based on location?
        query = db.emergency_dir.find({}).sort("distance",1).limit(1)
        for doc in query:
            db.put_counter.insert({"name":doc["name"],"aid":request.query.alexa, "endpoint":"emergency"})
            final = {"text" : [doc["name"], doc["address"], "is " + str(doc["distance"])+" miles away"]}
            return final

@get('/shelter_women')
def fun():
    query = db.shelter_dir.find({"type":"Women, Children"}).sort("distance",1)
    for doc in query:
        db.put_counter.insert({"name":doc["name"],"aid":request.query.alexa, "endpoint":"shelterwomen"})
        final = {"text" : [doc["name"], doc["address"], "is " + str(int(doc["distance"]))+" minutes away is the closest women friendly shelter"]}
        return final


@get('/emergency_children')
def fun():
    query = db.emergency_dir.find({"type":"Children"}).sort("distance",1).limit(1)
    for doc in query:
        db.put_counter.insert({"name":doc["name"],"aid":request.query.alexa, "endpoint":"emergencychildren"})
        final = {"text" : [doc["name"], doc["address"], "is " + str(doc["distance"])+" miles away"]}
        return final


@get('/hygiene')
#date
#location
#time
def returnarray():
   if db.hygiene_dir.count() == 0:
        rv = {"text": ["welcome-home", "111 legendary drive" , "has sanitary mapkins and is available all day"]}
        response.content_type = 'application/json'
        return dumps(rv)
   else:
        # How to sort the database? based on location?
        query = db.hygiene_dir.find({})
        for doc in query:
            db.put_counter.insert({"name":doc["location_name"],"aid":request.query.alexa, "endpoint":"hygiene"})
            final = {"text" : [" yes ","Sanitary napkins are available all day in the shelter"," there is also a "+ doc["type"] +" truck from " + doc["time"]+ " at "+doc["location_name"]]}
            return final


@get('/dashboard_shelter')
def returnarray():
    shelter_info=[]
    aid_list = db.alexa_locs.find()
    for row in aid_list:
        locations = []
        aid_counter = db.put_counter.find({"aid":str(int(row["aid"])),"endpoint":"shelter"}).count()
        locations = {"lat":row["lat"] ,"long":row["long"] , "count":int(aid_counter)}
        shelter_info.append(locations)
    #print shelter_info
    shelter_json = {"shelter":shelter_info}
    return shelter_json

@get('/dashboard_emergency')
def returnarray():
    emergency_info=[]
    aid_list = db.alexa_locs.find()
    for row in aid_list:
        locations = []
        aid_counter = db.put_counter.find({"aid":str(int(row["aid"])),"endpoint":"emergency"}).count()
        locations = {"lat":row["lat"] ,"long":row["long"] , "count":int(aid_counter)}
        emergency_info.append(locations)
    #print shelter_info
    emergency_json = {"emergency":emergency_info}
    return emergency_json

@get('/dashboard_hygiene')
def returnarray():
    hygiene_info=[]
    aid_list = db.alexa_locs.find()
    for row in aid_list:
        locations = []
        aid_counter = db.put_counter.find({"aid":str(int(row["aid"])),"endpoint":"hygiene"}).count()
        locations = {"lat":row["lat"] ,"long":row["long"] , "count":int(aid_counter)}
        hygiene_info.append(locations)
    #print shelter_info
    hygiene_json = {"hygiene":hygiene_info}
    return hygiene_json

@get('/sos')
def returnarray():

    if request.query.alexa:
         sosState = request.query.alexa
         db.info.insert({"message":sosState, "CreateDate": datetime.datetime.utcnow()})
         rv = { "success": "updated sos state"}
         response.content_type = 'application/json'
         return dumps(rv)
    else:
        sosState = ""
        query = db.info.find().limit(1)
        for doc in query:
            sosState = doc["message"]
        if sosState != "":
            aid_list = db.alexa_locs.find({"aid":int(sosState)})
            return str(aid_list[0]["lat"]) + "," + str(aid_list[0]["long"])
        else:
            return ""

run(host='50.97.82.230', port=8080, debug=True)
