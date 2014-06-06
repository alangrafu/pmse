from flask import Flask, render_template, redirect, request, jsonify, Response
from flask_cors import cross_origin
import rdflib
import sys
import json



def runSPARQL(query, mime="application/sparql-results+json"):
	mime2format = {}
	mime2format["application/sparql-results+json"] = "json"
	mime2format["text/csv"] = "csv"
	mime2format["application/sparql-results+xml"] = "xml"
	format = "json"
	mtype = "application/sparql-results+json"
	if mime in mime2format.keys():
		format = mime2format[mime]
		mtype = mime
	try:
		qres = g.query(query)
		return Response(response=qres.serialize(format=format),mimetype=mtype)
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

try:
	g = rdflib.Graph()
	g.parse(settings["file"], format="n3")
except:
	print "No RDF graph %s found. Aborting" %settings["file"]
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
		best = "application/json"
		if "output" in request.args:
			best = request.args["output"]
		else:
			best = request.accept_mimetypes.best_match(["application/sparql-results+json", "application/sparql-results+xml", "text/csv"])
		return runSPARQL(q, best)
	else:
		return render_template("sparql.html")

if __name__ == "__main__":
	app.run(port=settings["port"], debug=settings["debug"], host=settings["host"])
