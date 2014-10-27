from tpb import TPB
from tpb import CATEGORIES, ORDERS
import re
import inspect
import urllib
import requests
from pyquery import PyQuery as pq
from lxml import etree
import json
import utils

t = TPB('https://thepiratebay.org')

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def t411_auth(username, password):
	result_req = requests.post("http://api.t411.me/auth", {'username': username, 'password': password})
	return result_req.text

def make_dict_from_torrent(torrent):
	torrent_info = {}
	torrent_info["title"] = torrent.title
	torrent_info["size"] = torrent.size
	torrent_info["download_link"] = torrent.magnet_link
	torrent_info["url"] = "%s" % torrent.url
	return torrent_info

def make_dict_from_torrent_t411(torrent):	
	torrent_info = {}
	torrent_info["title"] = torrent["name"]
	torrent_info["size"] = sizeof_fmt(float(torrent["size"]))
	torrent_info["id"] = torrent["id"]
	return torrent_info

def get_torrents_tpb_by_query(query, offset):
	torrents = []	
	for torrent in t.search(query).order(ORDERS.SEEDERS.DES).page(offset):
		torrent_info = make_dict_from_torrent(torrent)
		#torrent_info["description"] = torrent.info
		torrents.append(torrent_info)
	global_torrents = torrents		
	return torrents

def get_torrents_t411_by_query(query, offset, authorization):
	torrents = []	
	result_req = requests.get('http://api.t411.me/torrents/search/' + query + '?offset=' + str(offset) + '&limit=30', headers={'Authorization': authorization})	
	for torrent in json.loads(result_req.text)["torrents"]:
		torrent_info = make_dict_from_torrent_t411(torrent)
		torrents.append(torrent_info)
	return torrents


def find_all_categories(path, acc, depth):		
	if depth == 0:
		return acc
	if inspect.isclass(eval(path)):
		for name in dir(eval(path)):
			if not name.startswith('_'):
				acc[-1]["categories"].append({"name": name, "categories":[], "path": path+"."+name, "has_children": inspect.isclass(eval(path+'.'+name))})
				find_all_categories(path+'.'+name, acc[-1]["categories"], depth-1)
	return acc

def get_category(categories, category, index):
	array_category = str(category).split(".")	
	for c in categories:
		array_c = c["path"].split(".")
		if array_c == array_category[:index]:
			if len(array_category) == index:
				return c
			else:
				return get_category(c["categories"], category, index+1)

def get_categories(children_of, depth):
	if depth < 0:
		depth = 0
	depth_children_of = len(children_of.split(".")) - 1
	all_categories = find_all_categories('CATEGORIES', [{"name": "CATEGORIES", "categories": [], "path": "CATEGORIES", "has_children": True}], depth + depth_children_of)[0]
	if(children_of == "CATEGORIES"):		
		return all_categories
	else:
		return get_category(all_categories["categories"], children_of, 2)

def get_top_100_t411(authorization):
	torrents = []
	result_req = requests.get('http://api.t411.me/torrents/top/100',  headers={'Authorization': authorization})
	print result_req.text
	for torrent in json.loads(result_req.text):
		print torrent
		torrent_info = make_dict_from_torrent_t411(torrent)
		torrents.append(torrent_info)
	return torrents


def get_torrents_per_category(category):
	torrents = []
	for torrent in t.top().category(eval(category)):
		if torrent != None:
			torrent_info = make_dict_from_torrent(torrent)
			torrents.append(torrent_info)		
	return torrents

def get_torrent_info_t411(torrent_id, authorization):
	torrent_info = {}
	result_req = requests.get('http://api.t411.me/torrents/details/' + torrent_id,  headers={'Authorization': authorization})
	torrent_info["description"] = json.loads(result_req.text)["description"]
	return torrent_info

def get_torrent_info_by_url(torrent_url):	
	torrent_info = {}
	r = requests.get(torrent_url)
	d = pq(r.text)
	torrent_info["description"] = d("pre").html()
	return torrent_info

def get_torrent_file(id, authorization):
	r = requests.get('http://api.t411.me/torrents/download/' + id,  headers={'Authorization': authorization})
	return {'magnet_link': utils.createMagnetLinkFromTorrent(r.content)}





