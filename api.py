from flask import Flask
from flask import request
from flask import Response
#from flask import jsonify
from flask.ext.cors import CORS
import tpb_utils as utils
import json

app = Flask(__name__)
app.debug = True
cors = CORS(app)

@app.route("/")
def home():
	routes = {}
	routes['search'] = '/torrents/search?q={query}'
	routes['top'] = '/torrents/top/<category>'
	routes['categories'] = '/categories'
	return Response(json.dumps(routes), mimetype='application/json')

@app.route("/torrents/search")
def search():
	query = request.args.get('q')
	offset = request.args.get('offset') if request.args.get('offset') else 0
	result =  utils.get_torrents_by_query(query, offset)
	return Response(json.dumps(result), mimetype='application/json')

@app.route("/categories")
def categories():
	children_of = request.args.get('children_of') if request.args.get('children_of') else 'CATEGORIES'
	depth = int(request.args.get('depth')) if request.args.get('depth') else 100
	categories = utils.get_categories(children_of, depth)	
	return Response(json.dumps(categories), mimetype='application/json')

@app.route("/torrents/top/<category>")
def torrentsPerCategory(category):
	tops = utils.get_torrents_per_category(category)
	return Response(json.dumps(tops), mimetype='application/json')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=9001)

