#!/usr/bin/python3
from flask import Flask, request
from flask_pymongo import PyMongo
import requests as req
import json
import user
app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)


# return user information
@app.route('/user/<username>')
def userpage(username):
    data = user.fetch_userdata_fromDB(username)
    return json.dumps(data)


# return book information
# TODO: 現状モックなので実際のISBNを対象に動くようにする
@app.route('/book/<isbn>')
def bookinfo(bookid):
    title = 'hoge'
    author = 'fuga'
    isbn = "0"
    publisher = 'piyo'

    data = {
        "bookid": bookid,
        "title": title,
        "author": author,
        "isbn": isbn,
        "publisher": publisher
    }
    return json.dumps(data)


# record reading status
@app.route('/record', methods=['POST'])
def record():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    username = data['username']
    status = data['status']
    isbn = data['isbn']
    a = user.update_userdata(username, status, isbn)
    return str(type(a))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
