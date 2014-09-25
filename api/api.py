from flask import request
from flask import Response
import tpb_utils as utils
import json
from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def home():
	print "route home"
	routes = {}
	routes['auth'] = '/auth/<tracker>'
	routes['search'] = '/torrents/<tracker>/search?q={query}'
	routes['top'] = '/torrents/<tracker>/top/<category>'
	routes['categories'] = '/categories/<tracker>'
	return Response(json.dumps(routes), mimetype='application/json')

@app.route("/auth/<tracker>", methods=['POST'])
def auth(tracker):
	if tracker == "t411":
		username = request.form['username']
		password = request.form['password']
		result = utils.t411_auth(username, password)
		return Response(result, mimetype='application/json')
	return Response(json.dumps("{}"), mimetype='application/json')

@app.route("/torrents/<tracker>/search")
def search(tracker):
	offset = request.args.get('offset') if request.args.get('offset') else 0
	query = request.args.get('q')
	if tracker == "t411":
		authorization = request.args.get('authorization')
		result = utils.get_torrents_t411_by_query(query, offset, authorization)		
	else:
		result = utils.get_torrents_tpb_by_query(query, offset)		
	return Response(json.dumps(result), mimetype='application/json')

@app.route("/torrents/<tracker>/info")
def info(tracker):
	id = request.args.get('id')
	torrent_info = {}
	if tracker == "t411":
		authorization = request.args.get('authorization')
		torrent_info = utils.get_torrent_info_t411(id, authorization)
	else:
		torrent_info = utils.get_torrent_info_by_url(id)
	return Response(json.dumps(torrent_info), mimetype='application/json')

@app.route("/categories/<tracker>")
def categories(tracker):
	if tracker == "t411":
		categories = {"path": "CATEGORIES", "name":"CATEGORIES", "has_children": True, "categories": 
		[{"path": "CATEGORIES.ALL", "has_children": False, "name": "ALL", "categories":[]}, {"path": "CATEGORIES.TOPS", "has_children": False, "name": "TOPS", "categories":[{"path": "CATEGORIES.TOP100", "has_children": False, "name": "TOP100", "categories":[]}]}]}
	else:
		children_of = request.args.get('children_of') if request.args.get('children_of') else 'CATEGORIES'
		depth = int(request.args.get('depth')) if request.args.get('depth') else 100
		categories = utils.get_categories(children_of, depth)	
	return Response(json.dumps(categories), mimetype='application/json')

@app.route("/torrents/<tracker>/top/<category>")
def torrentsPerCategory(tracker, category):
	if tracker == "t411":
		authorization = request.args.get('authorization')
		tops = utils.get_top_100_t411(authorization)
	else:
		tops = utils.get_torrents_per_category(category)
	return Response(json.dumps(tops), mimetype='application/json')

@app.route("/torrents/<tracker>/download/<id>")
def download(tracker, id):
	if tracker == "t411":
		authorization = request.args.get('authorization')
		torrent_file = utils.get_torrent_file(id, authorization)
		return Response(torrent_file, mimetype='application/x-bittorrent')
	return Response(None, mimetype='application/x-bittorrent')


if __name__ == '__main__':
        app.run(debug=True)
