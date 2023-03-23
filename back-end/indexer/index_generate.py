#!/usr/bin/env python

import os
import sys
sys.path.append('/Users/lidongyu/Desktop/recipe_search/back-end')
import json
import pickle

#import pandas as pd

import preprocessing
from db import database_functions
import argparse
import logging

batchnum = 247

logging.basicConfig(filename='result.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class IndexGenerator:  
    def __init__(self, activate_stemming = True, activate_stop = False, start_index=0):
        """ This class reaeds the documents from db, generates an inverted index and saves it into db.
        
        Keyword Arguments:
            activate_stemming {bool} -- True enables the stemming function over the terms (default: {True})
            activate_stop {bool} -- True enables removing stop words (default: {False})
        """
        self.activate_stemming = activate_stemming
        self.activate_stop = activate_stop
        self.start = start_index

        self.temp = dict()
        self.len_batch = []
        self.len = []
        self.avg_len = 0
    
    def run_indexing(self):
        """ This function gets the sentences from db and updates the inverted index in db by iterating the sentences.
        """

        batchsize = 10000 #read batchsize items everytime
        for i in range(self.start, batchnum):
            logging.info("loading: " + str(i+1) + "/" + str(batchnum))
            cursors = database_functions.get_recipe_cursors(i * batchsize, batchsize)
            for cursor in cursors:
                self.__load_tempfile(cursor.get('_id'),cursor.get('directions'))

            if (i+1)% 10 == 0:
                self.__regularize_dict()
                self.__save_pickle(str(i-9) + "-" + str(i+1) + "-insert")

            self.len.append(sum(self.len_batch)/len(self.len_batch))
            self.len_batch = []
        
        self.avg_len = sum(self.len)/len(self.len)
        print("****************************************************")
        print(self.avg_len)
        print("****************************************************")

        self.__regularize_dict()
        self.__save_pickle("last")

    def __load_tempfile(self, doc_id, directions):
        prep_directions = list(preprocessing.preprocess(directions, stemming=self.activate_stemming, stop=self.activate_stop))
        #preprocessed = list(filter(None, preprocessed))

        word_count = len(preprocessing.preprocess(directions, stemming=False, stop=False))
        self.len_batch.append(word_count)

        for term in set(prep_directions):
            positions = [n for n,item in enumerate(prep_directions) if item==term]
            self.temp[term] = self.temp.get(term, {
                'term': term,
                'doc_count': 0,
                'recipes': dict()
            }) #get can create a new item if the term does not exist
            self.temp[term]['doc_count'] += 1
            self.temp[term]['recipes'][doc_id] = self.temp[term]['recipes'].get(doc_id, {'_id': doc_id, 'doc_count': len(positions), 'len':word_count })

    def __regularize_dict(self):
        for value in self.temp.values():
            value['recipes'] = list(value['recipes'].values())

    def __save_pickle(self, name):
        with open(name + '.pickle', 'wb') as handle:
            pickle.dump(list(self.temp.values()), handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.temp.clear()

def run_with_arguments(stem, stop, start):
    print('Enter function run_-with_arguments')
    indexGen = IndexGenerator(activate_stop=stop, activate_stemming=stem, start_index=start)
    indexGen.run_indexing()

parser = argparse.ArgumentParser(description='Inverted Index Generator')
parser.add_argument('--stemming', nargs="?", type=str, default='True', help='Activate stemming')
parser.add_argument('--remove_stopwords', nargs="?", type=str, default='True', help='Remove stopwords')
parser.add_argument('--start', nargs="?", type=int, default=0, help='Start batch index')
args = parser.parse_args()



run_with_arguments(eval(args.stemming), eval(args.remove_stopwords), args.start)
