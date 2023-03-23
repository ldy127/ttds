from flask import Flask, jsonify
from flask import Flask, request, render_template, make_response, redirect, url_for
import json
from flask_cors import CORS
import pymongo
from bson import json_util
from keras.models import load_model
from pickle import load
import numpy as np
import os


# connect database
# 数据库名称
myDataBase = "test"
# 集合名称
myCollection = "recipe"
# 数据库通信证,换成你自己的
tooken = "mongodb+srv://faye:passwordforttds@cluster0.d0myq6k.mongodb.net/?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(tooken)
mydb = myclient[myDataBase]  # 数据库名称
indexer = mydb['inverted_index']
db_mongodb = mydb[myCollection]  # 集合名称

# run the neural network
# import sys
# sys.path.append('/Users/lidongyu/Desktop/recipe_search')
model_path = "/Users/lidongyu/Desktop/recipe_search/back-end/search/checkpoints/word_pred_Model3.h5"
# model_path = "../search/checkpoints/word_pred_Model3.h5"
model = load_model(model_path)
tokenizer = load(open("/Users/lidongyu/Desktop/recipe_search/back-end/tokenizer_Model3","rb"))
# tokenizer = load(open("../tokenizer_Model3"))
seq_len = 2
num_gen_words = 2


app = Flask(__name__)
CORS(app, resources=r'/*')  # 注册 CORS, "/*" 允许访问所有api

from search import routes
