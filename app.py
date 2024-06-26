from flask import Flask, request, Response, stream_with_context, jsonify
from redis import Redis
import socket
import os, time, json
app = Flask(__name__)
db = Redis(host='10.96.99.51', port=6379)
myip = socket.gethostbyname(socket.gethostname())
@app.route('/')
def hello():
    db.incr('count')
    return 'IP : ' + myip + '  Count is %s.' % db.get('count')


@app.route('/<path:path>', methods = ['PUT', 'GET'])
def home(path):

    if (request.method == 'PUT'):
        event = request.json
        event['last_updated'] = int(time.time())
        db.delete(path) #remove old keys
        db.hmset(path, event)
        return jsonify(event), 201


    if not db.exists(path):
        return "Error: path does not exist"

    event = db.hgetall(path)
    return jsonify(event), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)