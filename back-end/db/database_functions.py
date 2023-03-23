import pymongo
#import gridfs
import json

from pymongo import MongoClient
 

client = pymongo.MongoClient("mongodb+srv://faye:passwordforttds@cluster0.d0myq6k.mongodb.net/?retryWrites=true&w=majority")

 

db = client['data']

recipe = db.recipe
inverted_index = db.inverted_index


sentence_bson_list = list()
previous_id = -1

index_bson_list = list()

def get_max_sent_id():
    return recipe.find_one({"_id": {"$exists": True}}, sort=[("_id", -1)])["_id"]

def get_recipe_cursors(start, count):
    return recipe.find({}, limit=count, skip=start)



