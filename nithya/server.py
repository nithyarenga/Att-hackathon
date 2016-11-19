from bottle import route, run
from bottle import request, response
from bottle import post, get, put, delete
from pymongo import MongoClient
from json import dumps
from bson import json_util

client = MongoClient()
db = client.lighthouse

@get('/hello')
def hello():
    return "Hello World!"

@route('/m2x_trigger')
def m2x_trigger():
    return "hello"

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
    rv = [{ "name": "welcome-home", "address": "111 legendary drive"}, { "name": "dallas life foundation", "address": "1234 life street"}]
    response.content_type = 'application/json'
    return dumps(rv)


@get('/emergency')
#name
#address
def fun():
    pass

@get('/shelterwomen')
def fun():
    pass


@get('/emergencytypes')
def fun():
    pass


@get('/hygiene')
#date
#location
#time
def fun():
    pass

run(host='50.97.82.230', port=8080, debug=True)
