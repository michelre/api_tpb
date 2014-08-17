from flask import Flask
from flask import request
from flask import Response
#from flask import jsonify
from flask.ext.cors import CORS
import tpb_utils as utils
import json

app = Flask(__name__)
cors = CORS(app)

@app.route("/search")
def search():
	query = request.args.get('query')
	offset = request.args.get('offset') if request.args.get('offset') else 0
	result =  utils.get_torrents_by_query(query, offset)
	return Response(json.dumps(result), mimetype='application/json')

@app.route("/categories")
def categories():
	categories = utils.get_categories()
	return Response(json.dumps(categories), mimetype='application/json')

@app.route("/top100")
def top100():
	offset = request.args.get('offset') if request.args.get('offset') else 0
	utils.get_torrent_top(offset)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=9001)

