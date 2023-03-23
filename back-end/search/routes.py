from search import app, model, tokenizer, seq_len, num_gen_words
from flask import jsonify, request, session
from search.controller import getMongo, gen_text

from .controller import getMongo
from .controller import recipe_search
#from .spelling import SpellChecker
from search import db_mongodb
from math import log10
import numpy as np
import pandas as pd
from flask import Flask, Blueprint, render_template, redirect, url_for, session, request, jsonify
# from wtforms import Form, BooleanField, StringField, PasswordField, form, validators, DateField, RadioField, ValidationError, FileField, \
# DateField, FloatField, IntegerField, SelectField
import pymongo
#from flask_pymongo import PyMongo

import time
import re



# route for home page
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/test', methods=['GET','POST'])
def test():
    print("in")
    # 判断入参是否为空
    if request.method == "POST":
        
        post_data = request.get_json()
    # 获取传入的params参数
    dish = post_data.get('dish')
    print(dish)
    result = getMongo(dish)
    # 对参数进行操作
    return jsonify(result)

@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    if request.method == "POST":
        post_data = request.get_json()
    seed_text = post_data.get('input')
    result = []
    if (seed_text != ''):
        for i in range(-3,0):
            out = gen_text(model, tokenizer, seq_len=seq_len, seed_text=seed_text, num_gen_words=num_gen_words, first=i)
            print('Output: '+seed_text+' '+out)
            result.append(seed_text+' '+out)
    return jsonify({'suggestion': result})

@app.route('/index', methods=['GET','POST'])
def search():
    if request.method == "POST":
        post_data = request.get_json()

    dish = post_data.get('dish')
    included_ingr_str = post_data.get('include')
    excluded_ingr_str = post_data.get('exclude')
    searchType = post_data.get('searchType')

    include,exclude = [],[]

    include = [] if included_ingr_str == "" else re.split('[ ,]+',included_ingr_str)
    exclude = [] if excluded_ingr_str == "" else re.split('[ ,]+', excluded_ingr_str)
    print(include)

    

    

    # If search is identical to the last (e.g. new page), use session instead
    # if(
    #     len(request.session.get("recipe_pks", [])) > 0 and
    #     search_exp == request.session.get("search_exp") and
    #     included_ingr == request.session.get("included_ingr") and
    #     excluded_ingr == request.session.get("excluded_ingr") and
    #     must_have == request.session.get("must_have")
    # ):
    #     res = [Recipe.objects.get(pk=pk)
    #            for pk in request.session["recipe_pks"]]
    # else:
    res = recipe_search(query=dish,
                            include=include,
                            exclude=exclude,
                            searchType=searchType,
                        )

    # Save found recipe PKs for quick loading next pages
    #request.session["recipe_pks"] = [r.pk for r in res]
    # Save search parameters to determine a new search or not on next run
    #request.session["search_exp"] = search_exp
    #request.session["included_ingr"] = included_ingr
    #request.session["excluded_ingr"] = excluded_ingr
    #request.session["must_have"] = must_have
    # Filter by tag if any selected
    # Get paginator and current page
    # paginator = Paginator(res, 10)
    # page = paginator.get_page(page_number)

    # page = request.args.get('page', 1, type=int)  # 获取当前页数
    # your_query = CommodityModel.query
    # # current_app.config['PER_PAGE_COUNT']是在设置中定义的每页页数
    # pagination1 = your_query.filter_by(type=1).paginate(page1, per_page=app.config['PER_PAGE_COUNT'],
    #                                                     error_out=False)
    # conditional_query = pagination1.items  # 每页的数据


    # context = {

    #         "search_exp": search_exp,
    #         "included_ingr": included_ingr,
    #         "excluded_ingr": excluded_ingr,
    #         "must_have": must_have
    # }
    return jsonify({'result':res})

