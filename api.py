#!/usr/bin/python3
from flask import Flask, request
from flask_pymongo import PyMongo
import requests as req
import json
import user
import book
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)


# return user information
@app.route('/user/<username>')
def userdata(username):
    data = user.fetch_userdata_fromDB(username)
    return json.dumps(data)


# return user's reading status
@app.route('/user/<username>/<isbn>')
def reading_status(username, isbn):
    data = user.fetch_readingstatus(username, isbn)
    return json.dumps(data)


# return book information
@app.route('/book/<isbn>')
def bookinfo(isbn):
    data = book.fetch_bookinfo(isbn)
    return json.dumps(data)


# record reading status
@app.route('/record', methods=['POST'])
def record():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    username = data['username']
    status = data['status']
    isbn = data['isbn']
    return user.update_userdata(username, status, isbn)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
