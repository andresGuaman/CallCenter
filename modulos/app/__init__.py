from flask import Flask
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,ObjectId):
            return str(o)
        if isinstance(o,datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self,o)        


app = Flask(__name__)  
app.config['MONGO_URI']= 'mongodb+srv://agmr:123@callcenter.am91v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app.json_encoder = JSONEncoder
mongo = PyMongo(app)


