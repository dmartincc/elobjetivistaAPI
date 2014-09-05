import os, datetime, json, pprint
from bson import json_util
from datetime import datetime, timedelta
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify
from jinja2 import TemplateNotFound
from app import app

period = datetime.now() - timedelta(hours=6)

def get_db(db_name):
    from pymongo import MongoClient
    uri = 'mongodb://user:passw0rd@kahana.mongohq.com:10026/dev-ethinker'
    client = MongoClient(uri)
    db = client[db_name]
    return db  

@app.route("/api", methods=["GET","POST"])
def api():

	dic = {"name":"elobjetivista API",
		   "version":0.1,
		   "owner":"elobjetivista.com",
		   "datapoints":{
		   "trends":"/api/0.1/trends",
		   "articles":"/api/0.1/articles"}}
	return jsonify(dic)

@app.route("/api/0.1/articles", methods=["GET","POST"])
def articles():
	if request.args.get('num'):
		num = request.args.get('num')
	else:
		num = 20
	db = get_db('dev-ethinker')
	response={}
	documents=[]
	data = db.articles.find({"date":{"$gt": period}}).limit(num)
	for document in data:
		document['_id']=str(document['_id'])
		document['date']=str(document['date'])
		documents.append(document)	

	response['result']=documents
	response['num']=len(documents)
	return jsonify(response)

@app.route("/api/0.1/articles/<category>", methods=["GET","POST"])
def categories(category):
	db = get_db('dev-ethinker')	
	data = db.articles.find({"date":{"$gt": period},"tags":category})	
	response={}
	documents=[]

	for document in data:
		document['_id']=str(document['_id'])
		document['date']=str(document['date'])
		documents.append(document)	

	response['result']=documents
	return jsonify(response)

@app.route("/api/0.1/trends", methods=["GET","POST"])
def trends():
	db = get_db('dev-ethinker')
	response={}
	documents=[]
	data = db.trends.find().sort('date',-1).limit(1)	
	for document in data:
		document['_id']=str(document['_id'])
		document['date']=str(document['date'])
		documents.append(document)
		
	response['result']=documents
	
	return jsonify(response)