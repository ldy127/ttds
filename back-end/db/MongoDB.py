from typing import List
from flask_pymongo import PyMongo
from pymongo import MongoClient
from db.DBInterface import DBInterface
import gridfs
import json
import re
from operator import itemgetter
import time

class MongoDB(DBInterface):

    BULK_WRITE_LIMIT = 1000

    def __init__(self):
        super().__init__()
        #client = MongoClient('INSERT_YOUR_OWN_IP', 27017, username='INSERT_YOUR_OWN_USERNAME', password='INSERT_YOUR_OWN_PASSWORD')
        client = MongoClient("mongodb+srv://faye:passwordforttds@cluster0.d0myq6k.mongodb.net/?retryWrites=true&w=majority")
        self.test = client.test
        self.recipe = self.test.recipe
        self.inverted_index = self.test.inverted_index
        #self.movies = self.ttds.movies
        #self.movies.create_index('_id')
        #self.inverted_index_gridfs = gridfs.GridFS(self.ttds)

    def get_indexed_documents_by_term(self, term: str, sort_entries: bool = False):
        s1 = time.process_time()
        docs_for_term = self.inverted_index.find({"term": term}, {"_id": 0})
        if sort_entries:
            docs_for_term = docs_for_term.sort('recipes._id')
        #docs_for_term = docs_for_term.skip(skip).limit(limit)
        s2 = time.process_time()
        print("Time for get indexed document by term:")
        print(s2-s1)
        return docs_for_term

