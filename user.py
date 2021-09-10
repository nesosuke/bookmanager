#!/usr/bin/python3
import datetime
from flask import Flask
from flask_pymongo import PyMongo
app = Flask(__name__)

app.secret_key = "super secret string"  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config["JSON_AS_ASCII"] = False
mongo = PyMongo(app)


# create user into DB:bookmeter/status
def create_user(username):
    isExist = mongo.db.status.find_one({"username": username})
    if isExist is None:  # usernameに空きがある
        new_userdata = {"username": username}
        mongo.db.status.insert(new_userdata)
        result = "userdata is created!"
    else:
        result = "this username is not available."
    return result


# fetch user data from DB:bookmeter/status
def fetch_userdata_fromDB(username):
    res = list(mongo.db.status.find({"username": username}))

    num_read = 0
    num_reading = 0
    num_unread = 0
    num_wish = 0
    for d in res:
        if d['status'] == "read":
            num_read += 1
        elif d['status'] == "reading":
            num_reading += 1
        elif d['status'] == "unread":
            num_unread += 1
        elif d['status'] == "wish":
            num_wish += 1

    # やりたいけどできなかった
    # num_read = res.count({"status": "read"})
    # num_reading = res.count({"status": "reading"})
    # num_unread = res.count({"status": "unread"})
    # num_wish = res.count({"status": "wish"})

    data = {"username": username,
            "read": num_read,
            "reading": num_reading,
            "unread": num_unread,
            "wish": num_wish
            }
    return data


# update user data in DB:bookmeter/status
def update_userdata(username, status, isbn):
    search_arg = {
        "username": username,
        "isbn": isbn}
    data = {"$set":
            {
                "username": username,
                "status": status,
                "isbn": isbn,
                "record_at": str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])+'+09:00'
            }
            }
    mongo.db.status.find_one_and_update(search_arg, data, upsert=True)
    result = mongo.db.status.find_one(search_arg, {'_id': 0})
    return result


# fetch user's reading status by ISBN
def fetch_readingstatus(username, isbn):
    search_arg = {"username": username, "isbn": isbn}
    data = mongo.db.status.find_one(search_arg, {'_id': 0})
    if data is None:
        mongo.db.status.find_one_and_update(search_arg,
                                            {"$set":
                                             {"username": username,
                                              "isbn": isbn,
                                              "status": "unread"}, }, upsert=True
                                            )
    return data
