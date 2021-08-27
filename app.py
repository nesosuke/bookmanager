#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
import requests as req
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)


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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
