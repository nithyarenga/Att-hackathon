from bottle import route, run
from bottle import request, response
from bottle import post, get, put, delete
from pymongo import MongoClient
from json import dumps
from bson import json_util
from m2x.client import M2XClient
from datetime import datetime
from requests.exceptions import HTTPError

client = MongoClient()
db = client.lighthouse

client = M2XClient(key="dbbbb260442d2411fb43e2f1917a8d88")

@get('/hello')
def hello():
    return "Hello World!"

@route('/m2x_trigger')
def m2x_trigger():
    # Find the correct device if it exists, if not create it.
    try:
        device = [d for d in client.devices(q="stockreport-bluemix") if d.name == "stockreport-bluemix"][0]
    except IndexError:
        device = client.create_device(name="stockreport-bluemix",
                                      description="Stockreport Example Device",
                                      visibility="private")

    # Get the stream if it exists, if not create the stream.
    stream = device.stream("counter")
    postime = datetime.now()
    stream.add_value(db.put_counter.count(), postime)
    #import ystockquote
    #stock_price = ystockquote.get_price("T").encode('utf-8')
    #stream.add_value(stock_price, postime)
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
    if db.shelter_dir.count() == 0:
        rv = [{ "name": "welcome-home", "address": "111 legendary drive"}, { "name": "dallas life foundation", "address": "1234 life street"}]
        response.content_type = 'application/json'
        return dumps(rv)
    else:
        # How to sort the database? based on location?
        query = db.alerts.find()
        for doc in query:
            return json_util.dumps(doc)


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
