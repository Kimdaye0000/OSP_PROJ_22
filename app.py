#!/usr/bin/python
#-*-coding: utf-8 -*-

from flask import Flask, render_template, redirect
import re
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def web1():
	return redirect("https://jfk3ow.axshare.com/#id=so8yho&p=main")
	

if __name__ == '__main__':
	app.run(debug=True)
