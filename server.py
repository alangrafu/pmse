from flask import Flask, render_template, redirect, request, jsonify, Response
from flask_cors import cross_origin
import rdflib
import sys
import json


rdfFile = "a.ttl"
port = 8890
g = None
debug = False

def runSPARQL(query):
	try:
		qres = g.query(query)
		return Response(response=qres.serialize(format="json"),mimetype="application/json")
	except:
		print sys.exc_info()
		return jsonify(msg= "Error in SPARQL query"), 400

try:
	with open("settings.json", "r") as f:
		settings = json.load(f)
except:
	print sys.exc_info()
 	print "Can't find settings.json. Aborting."
 	exit(1)

if "file" in settings:
 	rdfFile = settings["file"]
if "port" in settings:
 	port = settings["port"]
if "debug" in settings:
	debug = settings["debug"]
try:
	g = rdflib.Graph()
	g.parse(rdfFile, format="n3")
except:
	print "No RDF graph %s found. Aborting" %rdfFile
	exit(2)

app = Flask(__name__)

@app.route("/")
def r():
	return redirect("/sparql", 301)

@app.route("/sparql")
@cross_origin()
def hello():
	if "query" in request.args:
		q =  request.args["query"]
		return runSPARQL(q)
	else:
		return render_template("sparql.html")

if __name__ == "__main__":
	app.run(port=port, debug=debug)
