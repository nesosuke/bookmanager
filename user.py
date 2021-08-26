#!/usr/bin/python3
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
        new_userdata = {
            "username": username,
            "read": 0,
            "reading": 0,
            "unread": 0,
            "wish": 0,
        }
        mongo.db.status.insert(new_userdata)
        result = "userdata is created!"
    else:
        result = "this username is not available."
    return result


# fetch user data from DB:bookmeter/status
def fetch_userdata_fromDB(username):
    data = mongo.db.status.find_one({"username": username})
    return data


# update user data in DB:bookmeter/status
