#!/usr/bin/python
#-*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request
from elasticsearch import Elasticsearch
from travelinfo_pkg import *

es_host ="http://localhost:9200"
index_countryinfo = "countryinfo"
index_searchpopularity = "searchpopularity"

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
	return render_template('index.html')
	
@app.route('/info', methods=['GET'])
def info():
	if request.method == 'GET':
		country = request.args.get('country')

		countryInfoDocument = crawlCountryInfo(country)
		if countryInfoDocument != None:
			insertToIndex(es, index_countryinfo, country, countryInfoDocument)
		else:
			query = { "query": { "bool": { "filter": [ { "match_phrase": { "Country": country } } ] } } }
			countryInfoDocument = searchFromIndex(es, index_countryinfo, query)
		
		searchPopularDoc = crawlSearchPopularity(country)
		if searchPopularDoc != None:
			insertToIndex(es, index_searchpopularity, country, searchPopularDoc)
		else:
			query = { "query": { "bool": { "filter": [ { "match_phrase": { "Country": country } } ] } } }
			searchPopularDoc = searchFromIndex(es, index_searchpopularity, query)

		if countryInfoDocument != None and searchPopularDoc != None:
			return render_template('info.html', data=countryInfoDocument, data2=searchPopularDoc)
		else:
			return render_template('error.html', country=country)

if __name__ == '__main__':

	es = Elasticsearch(es_host)

	createIndex(es, index_countryinfo)
	createIndex(es, index_searchpopularity)

	app.run(debug=True)
