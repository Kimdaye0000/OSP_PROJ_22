#!/usr/bin/python
#-*-coding: utf-8 -*-

from flask import Flask, render_template, redirect, request
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from travelinfo_pkg import *

es_host ="http://localhost:9200"
index_countryinfo = "countryinfo"
index_searchpopularity = "searchpopularity"

app = Flask(__name__)

@app.route("/", methods=['POST'])
def index():
	return render_template('index.html')
	
@app.route('/info', methods=['GET'])
def info():
	if request.method == 'GET':
		country = request.args.get('country')
		countryInfoDocument = crawl(country)
		if countryInfoDocument != None:
			insertToIndex(es, index_countryinfo, country, countryInfoDocument)
			return render_template('info.html', data=countryInfoDocument)
		else:
			query = { "query": { "bool": { "filter": [ { "match_phrase": { "Country": country } } ] } } }
			searchRes = searchFromIndex(es, index_countryinfo, query)
			if searchRes != None:
				return render_template('info.html', data=searchRes)
			else:
				return render_template('error.html', data=country)

if __name__ == '__main__':

	es = Elasticsearch(es_host)

	createIndex(es, index_countryinfo)
	createIndex(es, index_searchpopularity)

	#app.run(debug=True)
