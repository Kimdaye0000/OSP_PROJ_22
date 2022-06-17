#!/usr/bin/python
#-*-coding: utf-8 -*-

from flask import Flask, render_template, redirect
import re
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def index():
	return redirect("https://jfk3ow.axshare.com/#id=so8yho&p=main")
	
@app.reute('/info', methods=['GET'])
def info:
	if request.method == 'GET':
		myname = request.args.get('name')
		return render_template('info.thml', name=myname)

if __name__ == '__main__':
	app.run(debug=True)
