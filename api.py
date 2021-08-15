#!/usr/bin/python3

from flask import Flask
from flask_pymongo import PyMongo
import json
app = Flask(__name__)

app.secret_key = 'super secret string'  # Change this!
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookmeter"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)


# return user information
@app.route('/user/<username>')
def userpage(username):
    number_read = 0
    number_reading = 0
    number_unread = 0
    number_wish = 0

    data = {
        "username": username,
        "read": number_read,
        "reading": number_reading,
        "unread": number_unread,
        "wish": number_wish,
    }
    return json.dumps(data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
