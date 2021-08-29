#!/usr/bin/python3
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import requests
import user
import book
import json

app = Flask(__name__)
CORS(app)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)


# Webpages section
# return toppage
@app.route('/')
def toppage():
    return render_template('index.html')


# return search page
@app.route('/search')
def search_page():
    return render_template('search.html')


# return camera page
@app.route('/camera')
def camera_page():
    return render_template('camera.html')


# API section
# return user information
@app.route('/api/v1/user/<username>')
def userdata(username):
    data = user.fetch_userdata_fromDB(username)
    return json.dumps(data)


# return user's reading status
@app.route('/api/v1/user/<username>/<isbn>')
def reading_status(username, isbn):
    data = user.fetch_readingstatus(username, isbn)
    return json.dumps(data)


# return book information
@app.route('/api/v1/book/<isbn>')
def bookinfo(isbn):
    data = book.fetch_bookinfo(isbn)
    return json.dumps(data)


# record reading status
@app.route('/api/v1/record', methods=['POST'])
def record():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    username = data['username']
    status = data['status']
    isbn = data['isbn']
    return user.update_userdata(username, status, isbn)


# search ISBN from DB
@app.route('/api/v1/book/search')
def search_ISBN():
    query = request.args.get('title')
    data = json.dumps(book.search_ISBN(query))
    return data


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
