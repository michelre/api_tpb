from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.cors import CORS
import tpb_utils as utils

app = Flask(__name__)
cors = CORS(app)

@app.route("/search")
def search():
	query = request.args.get('query')
	offset = request.args.get('offset') if request.args.get('offset') else 0
	return jsonify(utils.get_torrents_by_query(query, offset))

if __name__ == "__main__":
	app.run(port=10001)

