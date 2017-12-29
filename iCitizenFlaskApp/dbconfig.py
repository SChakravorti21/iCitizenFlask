from pymongo import MongoClient
from os import environ

client = MongoClient(environ['ICITIZEN_MONGODB_URI'])
db = client['icitizen']