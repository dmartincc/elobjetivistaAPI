import os, datetime, json, pprint
from datetime import datetime, timedelta
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify
from jinja2 import TemplateNotFound
from app import app
from bson.objectid import ObjectId 

period = datetime.now() - timedelta(hours=6)

def get_db(db_name):
    from pymongo import MongoClient
    uri = 'mongodb://user:passw0rd@kahana.mongohq.com:10026/dev-ethinker'
    client = MongoClient(uri)
    db = client[db_name]
    return db  

@app.route("/", methods=["GET","POST"])
def api():

	dic = {"name":"elobjetivista-API",
		   "version":0.1,
		   "owner":"elobjetivista.com",
		   "datapoints":{
		   "trends":"/trends",
		   "articles":"/articles"}}
	return jsonify(dic)

@app.route("/articles", methods=["GET","POST"])
def articles():
	if request.args.get('num'):
		num = request.args.get('num')
	else:
		num = 20
	response={}
	documents=[]
	db = get_db('dev-ethinker')
	data = db.articles.find({"date":{"$gt": period}}).limit(num).sort("date",-1)
	for document in data:
		document['_id']=str(document['_id'])
		document['date']=str(document['date'])
		documents.append(document)	

	res = jsonify(items=documents)
	res.headers['Access-Control-Allow-Origin'] = '*'
	return res

@app.route("/articles/id/<idnum>", methods=["GET","POST"])
def article(idnum):
	response={}
	documents=[]
	db = get_db('dev-ethinker')
	data = db.articles.find({"_id":ObjectId(idnum)})
	for document in data:
		document['_id']=str(document['_id'])
		document['date']=str(document['date'])
		documents.append(document)	

	res = jsonify(items=documents)
	res.headers['Access-Control-Allow-Origin'] = '*'
	return res

@app.route("/articles/<category>", methods=["GET","POST"])
def categories(category):
	db = get_db('dev-ethinker')	
	data = db.articles.find({"date":{"$gt": period},"tags":category}).sort("date",-1)	
	response={}
	documents=[]

	for document in data:
		document['_id']=str(document['_id'])
		document['date']=str(document['date'])
		documents.append(document)	

	res = jsonify(items=documents)
	res.headers['Access-Control-Allow-Origin'] = '*'
	return res

@app.route("/trends", methods=["GET","POST"])
def trends():	
	response={}
	documents=[]
	db = get_db('dev-ethinker')
	data = db.trends.find().sort('date',-1).limit(1)	
	for document in data:
		document['_id']=str(document['_id'])
		document['date']=str(document['date'])
		documents.append(document)
		
	res = jsonify(items=documents)
	res.headers['Access-Control-Allow-Origin'] = '*'
	return res