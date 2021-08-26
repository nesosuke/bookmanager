#!/usr/bin/python3
from flask import Flask, json
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
import json
import requests

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def bs4totext(bs4object, default_value=""):
    if bs4object is None:
        return default_value
    else:
        return bs4object.text


# fetch book info from DB:bookmeter/book
def fetch_bookinfo(isbn):
    bookinfo = mongo.db.book.find_one({"isbn": isbn})
    if bookinfo is None:
        url = 'https://iss.ndl.go.jp/api/opensearch?' + 'isbn=' + isbn
        res = BeautifulSoup(requests.get(url, verify=False).content,
                            'lxml', from_encoding='utf-8').channel.find('item')

        title = bs4totext(res.find('dc:title'))
        author = bs4totext(res.find('dc:creator'))
        series = bs4totext(res.find('dcndl:seriestitle'))
        volume = bs4totext(res.find('dcndl:volume'))
        publisher = bs4totext(res.find('dc:publisher'))
        permalink = bs4totext(res.find('guid'))

        mongo.db.book.find_one_and_update(
            {'isbn': isbn},
            {
                "$set":
                {
                    "title": title,
                    "author": author,
                    "series": series,
                    "volume": volume,
                    "publisher": publisher,
                    "permalink": permalink,
                },
            },
            upsert=True
        )
        bookinfo = mongo.db.book.find_one({'isbn': isbn})
    del bookinfo['_id']
    return bookinfo
