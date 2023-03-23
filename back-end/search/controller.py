import requests
import re
from flask import jsonify, request, session, json
from bson import json_util

from keras_preprocessing.sequence import pad_sequences
from keras.models import load_model
from pickle import load
import numpy as np
import os
from search import db_mongodb
import random
from collections import defaultdict
# from .spelling import SpellChecker
#import requests
import re
from flask import jsonify, request, session, json
from bson import json_util
import pymongo
from math import log10
import numpy as np
import pandas as pd
from flask import Flask, Blueprint, render_template, redirect, url_for, session, request, jsonify
import pymongo
from flask_pymongo import PyMongo
import sys
sys.path.append('/afs/inf.ed.ac.uk/user/s24/s2405466/Desktop/recipe_search-master/back-end')
from db.DB import get_db_instance
from search import preprocessing
import time
from math import floor

MAX_INDEX_SPLITS = 52  # maximum number of different entries in the inverted_index with the same term
TOTAL_NUMBER_OF_SENTENCES = 77584425
MAX_QUERY_TIME = 10  # max seconds to allow the query to run for
MAX_TERM_TIME = 4000000
batch_size = 20
db = get_db_instance()
TEMP_WHOLE_DATA = 50000
TEMP_DOC_NUM = 100
DOCNUM_PER_LIMIT = 42

def getMongo(dish):
    # 链接 MongoDB atlas
    myquery = {"title": dish}  # 查询条件
    mydoc = db_mongodb.find(myquery)  # 查询结果
    print(mydoc)
    # 取出其中的数据格式为json
    for x in mydoc:
        # 将x转换为对象
        x = json.loads(json_util.dumps(x))
        print(x)
        return x

def recipe_search(query="", include=[], exclude=[], searchType="directions"):

    result, len_i, len_e = [], len(include), len(exclude)
    limit_num = len_e + len_i
    n = floor(DOCNUM_PER_LIMIT * 2 **(limit_num/2))
    
    if searchType =='directions':
        # s1 = time.process_time()
        if len(query) == 0:
            temp = db_mongodb.find({},{'_id':0}).limit(n)
            for r in temp:
                result.append(r)
            
        else:   
            res = RankedSearch().search(query)
            for r in res[:n]:
                item = db_mongodb.find({'_id':r},{'_id':0}).hint('_id_')
                for i in item:
                    result.append(i)
        # s2 = time.process_time()
        # print("Time for get item from recipe")
        # print(s2-s1)

    elif searchType == 'dish':
        # my_dish = re.compile(f"(.*({ingr_reg})+){{{len_i},}}.*")
        res = db_mongodb.find({'lower title': query.lower()},{'_id':0}).hint('lower title_1')

        for r in res:
            if(len(result))<n: result.append(r)
            else: break

    if len_i !=0:
        for i in range(len_i):
            if i==0: ingr_reg = str(include[i])
            else: ingr_reg += '|' +str(include[i])
        
        my_ingredients = re.compile(f"(.*({ingr_reg})+){{{len_i},}}.*")

        result1 = []

        for i in range(len((result))):
            if re.match(my_ingredients, result[i]['ingredients']): result1.append(result[i])

        result = result1           

    if len_e !=0:
        for i in range(len_e):
            if i==0: excl_reg = str(exclude[i])
            else: excl_reg += '|' +str(exclude[i])
        
        my_ingredients = re.compile(f"(.*({excl_reg})+){{{len_e},}}.*")

        result1 = []

        for i in range(len((result))):
            if not re.match(my_ingredients, result[i]['ingredients']): result1.append(result[i])

        result = result1

    for i in range(len(result)):
        result[i]['ingredients'] = eval(result[i]['ingredients'])
        result[i]['directions'] = eval(result[i]['directions'])

    return result
    
   
    # if searchType == "dish":
    #     if len(include) == 0 and len(exclude) == 0:
    #         recipe_ids = None
    #     else:
    #         recipe_ids = BooleanIngredientSearch().search(include=include,
    #                                                       exclude=exclude)

    #     if len(query) == 0:
    #         random.seed(10)
    #         res = list(recipe_ids) if recipe_ids is not None else []
    #         random.shuffle(res)
    #     else:


    #     if recipe_ids is not None:

    #         res = [recipe_id for recipe_id in res if recipe_id in recipe_ids]

    #     return res[:count]





class BooleanIngredientSearch:
    def _get_recipes_with_ingr(self, ingr):
        """
        Finds all recipes with an ingredient which has the given ingredient as substring
        """
        result = []
        my_ingredients = re.compile(f"[a-z,A-Z,']*{ingr}[a-z,A-Z,']*")
        Recipe_Ingredient = db_mongodb.find({'ingredients':{"$regex":my_ingredients}})
        for x in Recipe_Ingredient:
            result.append(x)

        return result

    def search(self, include=[], exclude=[]):
        res, re_include, re_exclude= [],[],[]
        final_include, final_exclude = set(), set()

        if len(include) == 0:
            res = list(db_mongodb.find().pretty())


        for i ,ingredient in enumerate(include):
            re_include.append(self._get_recipes_with_ingr(ingredient.lower()))
            if i == 0: final_include = set(re_include[i])
            else: final_include |= set(re_include[i])
    
        for j, ingredient in enumerate(exclude):
            re_exclude.append(self._get_recipes_with_ingr(ingredient.lower()))
            if j == 0: final_include = set(re_exclude[j])
            else: final_exclude |= set(re_exclude[j])
            #res -= recipes_with_ingr
        
        if len(final_include)==0:
            cursor = db_mongodb.find().limit(TEMP_WHOLE_DATA)
            for i in cursor:
                final_include.add(i)
        if len(final_exclude)!=0:
            final_include = final_include - final_exclude

        return final_include


class RankedSearch:
    
    def __init__(self):
        #self.indexer = Indexer()
        # self.spell_checker = SpellChecker()
        self.AVG_LENGTH = 50
        self.DOC_COUNT = 7000000

    def search(self, query):
        def bm25_weights_vector(tfs, df, lengths, k=1.5):
            tf_components = np.array(tfs / (k * lengths / self.AVG_LENGTH + tfs + 0.5))
            idf_component = np.log10((self.DOC_COUNT - df + 0.5) / (df + 0.5))
            return tf_components * idf_component

        #tokens = self.indexer._preprocess_text(query)
        tokens = preprocessing.preprocess(query, stemming=1, stop=1)

        # Correct the spelling of the tokens
        #tokens = self.spell_checker.correct_spelling(tokens)

        scores = defaultdict(float)

        for token in tokens:
            recipe_ids, df, tfs, lengths = [], 0, [], []
            list_of_splitted = db.get_indexed_documents_by_term(token)

            for list in list_of_splitted:
                df += list['doc_count']
                for recipe in list['recipes']:
                    tfs.append(recipe['doc_count'])
                    lengths.append(recipe['len'])
                    recipe_ids.append(recipe['_id'])

            tfs = np.array(tfs)
            lengths = np.array(lengths)
            recipe_ids = np.array(recipe_ids)
                

            weights = bm25_weights_vector(tfs, df, lengths)
            # print(time.time() - start_time)

            # start_time = time.time()
            for i in range(len(recipe_ids)):
                scores[recipe_ids[i]] = weights[i]

            # Find the document frequency (df) from the inverted index
            # start_time = time.time()
            # df = Token.query.get(Token.title == token).recipe_count
            # print(time.time() - start_time)

            # start_time = time.time()
            # res = (RecipeTokenFrequency.query.filter(RecipeToken.token__title == token)
            #                                    .values("recipe", "in_title", "tf", "recipe_length"))
            # # print(time.time() - start_time)

            # # start_time = time.time()
            # res = pd.DataFrame.from_records(res)
            # recipe_ids = res["recipe"]
            # in_titles = res["in_title"]
            # tfs = res["tf"]
            # lengths = res["recipe_length"]
            # # print(time.time() - start_time)

            # start_time = time.time()

            # print(time.time() - start_time)

        return [x[0] for x in sorted(scores.items(), key=lambda item: item[1], reverse=True)]
    
def gen_text(model, tokenizer, seq_len, seed_text, num_gen_words, first):
    output_text = []
    input_text = seed_text
    for i in range(num_gen_words):
        encoded_text = tokenizer.texts_to_sequences([input_text])[0]
        pad_encoded = pad_sequences([encoded_text], maxlen=seq_len,truncating='pre')
        pred_word_ind = np.argsort(model.predict(pad_encoded))[-1][first]
        pred_word = tokenizer.index_word[pred_word_ind]
        input_text += ' '+pred_word
        output_text.append(pred_word)
    return ' '.join(output_text)
