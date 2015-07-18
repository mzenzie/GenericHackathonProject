import pymongo
import language
from pymongo import MongoClient

client = MongoClient("localhost", 12321)

db = client["advisor_database"]

languages  = db["languages"]

languages.insert_many(language.core_langauges)
