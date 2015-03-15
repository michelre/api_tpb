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
	routes = {}
	routes['auth'] = '/auth/<tracker>'
	routes['search'] = '/torrents/<tracker>/search?q={query}'
	routes['info'] = '/torrents/<tracker>/info?id={id}'
	routes['top'] = '/torrents/<tracker>/top/<category>'
	routes['categories'] = '/categories/<tracker>'	
	return Response(json.dumps(routes), mimetype='application/json')

@app.route("/auth/<tracker>", methods=['POST', 'OPTIONS'])
def auth(tracker):
	print "POST"
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
	authorization = request.args.get('authorization')
	result = utils.get_torrents_by_query(tracker, query, offset, authorization)
	return Response(json.dumps(result), mimetype='application/json')

@app.route("/torrents/<tracker>/info/<id>")
def info(tracker, id):
	torrent_info = ''
	if tracker == "t411":
		authorization = request.args.get('authorization')
		torrent_info = utils.get_torrent_info_t411(id, authorization)
	else:
		torrent_info = utils.get_torrent_info_torrent_hunter(id)
	return Response(json.dumps({'details' : torrent_info}), mimetype='application/json')

@app.route("/categories/<tracker>")
def categories(tracker):
	if tracker == "t411":
		categories = {"path": "CATEGORIES", "name":"CATEGORIES", "has_children": True, "categories": 
		[{"path": "CATEGORIES.ALL", "has_children": False, "name": "ALL", "categories":[]}, {"path": "CATEGhostIES.TOPS", "has_children": False, "name": "TOPS", "categories":[{"path": "CATEGORIES.TOP100", "has_children": False, "name": "TOP100", "categories":[]}]}]}
	else:
		children_of = request.args.get('children_of') if request.args.get('children_of') else 'CATEGORIES'
		depth = int(request.args.get('depth')) if request.args.get('depth') else 100
		categories = utils.get_categories(children_of, depth)	
	return Response(json.dumps(categories), mimetype='application/json')

@app.route("/torrents/<tracker>/tops")
def torrentsPerCategory(tracker):
	authorization = request.args.get('authorization')
	tops = utils.get_tops(tracker, authorization)
	return Response(json.dumps(tops), mimetype='application/json')

@app.route("/torrents/<tracker>/download/<id>")
def download(tracker, id):
	if tracker == "t411":
		authorization = request.args.get('authorization')
		magnet_link = utils.get_torrent_file_t411(id, authorization)
		return Response(json.dumps(magnet_link), mimetype='application/json')
	if tracker == 'torrent-hunter':
		id_splitted = id.split("_")
		magnet_link = utils.get_torrent_file_torrent_hunter(id_splitted[0], id_splitted[1])
		return Response(json.dumps(magnet_link), mimetype='application/json')
	return Response(None, mimetype='application/json')


if __name__ == '__main__':
        #app.run(debug=True, host='0.0.0.0')
        app.run(debug=False)
