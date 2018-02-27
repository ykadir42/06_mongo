'''
Jawad Kadir and Ibnul Jahan
SoftDev2 pd7
K06 -- Ay Mon, Go Git It From Yer Flask
2018-02-26

Data: Giphy - Make it Rain
http://api.giphy.com/v1/gifs/search?q=make+it+rain&api_key=dc6zaTOxFJmzC
We took the json file and went through it with the use of urllib2. We then added everything to the database.
'''

from flask import Flask, render_template, request
from pymongo import MongoClient
import urllib2
import json

c = MongoClient('lisa.stuy.edu')
c.drop_database('The_Cult_of_Mongod')
makeit = c.The_Cult_of_Mongod
makeitrain = makeit.makeitrain


#Gets the json information from the url
def get_gifs(url):
	data_file = urllib2.urlopen(url)
	info = data_file.read()
	d = json.loads(info)["data"]
	#print d
	return d
gifs = get_gifs("http://api.giphy.com/v1/gifs/search?q=make+it+rain&api_key=dc6zaTOxFJmzC")

#adds all the information to the database
def add_gifs(datas):
	makeitrain.insert_many(datas)
add_gifs(gifs)

#Searches through the database based on file type (even though they should all be gifs)
def search_by_type(type):
	print("This is all the matches of the file type " + type)
	matches = makeitrain.find({"type": type})
	# for i in matches:
	# 	print(i)
	return matches
#Searches the database based on who originally sent in the gif (must be in www.<source>.com format
def search_by_source(source):
	print("This is all the matches from the course " + source)
	matches = makeitrain.find({"source_tld": source})
	# for i in matches:
	# 	print(i)
	return matches
#Searches the database based on what the name of the gif is (This is a very specific name)
def search_by_title(title):
	print("This is all the matches from the title " + title)
	matches = makeitrain.find({"title": title})
	# for i in matches:
	# 	print(i)
	return matches

#-------------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/result", methods=["GET"])
def result():
	print request.args["search"]
	if(request.args["search"] == "file"):
		matches = search_by_type(request.args["query"])
	elif(request.args["search"] == "source"):
		matches = search_by_source(request.args["query"])
	elif(request.args["search"] == "title"):
		matches = search_by_title(request.args["query"])
	else:
		return render_template("index.html")
	return render_template("result.html", matches = matches)

if __name__ == '__main__':
	app.debug = True
	app.run()