#!/usr/bin/python3
from flask import Flask
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
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
    bookinfo = mongo.db.book.find_one({"isbn": isbn}, {'_id': 0})
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
        edition = bs4totext(res.find('dcndl:edition'))

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
                    "edition": edition,

                },
            },
            upsert=True
        )
        bookinfo = mongo.db.book.find_one({'isbn': isbn}, {'_id': 0})
    return bookinfo


# search ISBN by booktitle via curl
def get_ISBN_fromNDL(title):
    url = 'https://iss.ndl.go.jp/api/opensearch?' + \
        'cnt=' + str(20) + '&' + 'title=' + str(title)
    res = requests.get(url, verify=False)
    reslist = BeautifulSoup(
        res.content, 'lxml').channel.find_all('item')  # list
    bookinfolist = []
    for res in reslist:
        bookinfolist.append({'isbn': bs4totext(res.find('dc:identifier')),
                             'title': bs4totext(res.find('dc:title')),
                             'author': bs4totext(res.find('dc:creator')),
                             'series': bs4totext(res.find('dcndl:seriestitle')),
                             'volume': bs4totext(res.find('dcndl:volume')),
                             'publisher': bs4totext(res.find('dc:publisher')),
                             'permalink': bs4totext(res.find('guid')),
                             'edition': bs4totext(res.find('dcndl:edition')),
                             })  # list
    for i in range(len(bookinfolist)):
        mongo.db.book.find_one_and_update(
            {'isbn': bookinfolist[i]['isbn']},
            {
                "$set":
                {
                    "title": bookinfolist[i]['title'],
                    "author": bookinfolist[i]['author'],
                    "series": bookinfolist[i]['series'],
                    "volume": bookinfolist[i]['volume'],
                    "publisher": bookinfolist[i]['publisher'],
                    "permalink": bookinfolist[i]['permalink'],
                    "edition": bookinfolist[i]['edition'],
                },
            },
            upsert=True
        )
    return bookinfolist  # json


# search ISBN from DB:bookmeter/book
def search_ISBN(title):
    result = mongo.db.book.find({'title': {'$regex': title}}, {'_id': 0})
    resultlist = []
    for r in result:
        resultlist.append(r)
    return resultlist
