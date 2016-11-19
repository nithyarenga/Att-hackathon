from bottle import route, run
from bottle import request, response
from bottle import post, get, put, delete


@get('/hello')
def hello():
    return "Hello World!"

@route('/m2x_trigger')
def m2x_trigger():
    return "hello"

@get('/alert')
def returnarray():
    from json import dumps
    rv = [{ "id": 1, "name": "Test Item 1" }, { "id": 2, "name": "Test Item 2" }]
    response.content_type = 'application/json'
    return dumps(rv)

run(host='50.97.82.230', port=8080, debug=True)

