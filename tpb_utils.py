from tpb import TPB
from tpb import CATEGORIES, ORDERS
import re
import inspect

t = TPB('https://thepiratebay.org')

def make_dict_from_torrent(torrent):
	torrent_info = {}
	torrent_info["title"] = torrent.title
	torrent_info["size"] = torrent.size
	torrent_info["download_link"] = torrent.magnet_link
	return torrent_info

def get_torrents_by_query(query, offset):
	torrents = []	
	for torrent in t.search(query).order(ORDERS.SEEDERS.DES).page(offset):
		torrent_info = make_dict_from_torrent(torrent)
		torrents.append(torrent_info)
	return torrents


def find_all_categories(path, acc, depth):		
	if depth == 0:
		return acc
	if inspect.isclass(eval(path)):
		for name in dir(eval(path)):		
			if not name.startswith('_'):
				acc[-1]["categories"].append({"name": name, "categories":[], "path": path+"."+name})
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
	all_categories = find_all_categories('CATEGORIES', [{"name": "CATEGORIES", "categories": [], "path": "CATEGORIES"}], depth + depth_children_of)[0]
	if(children_of == "CATEGORIES"):		
		return all_categories
	else:
		return get_category(all_categories["categories"], children_of, 2)

def get_torrents_per_category(category):
	torrents = []
	for torrent in t.top().category(eval(category)):
		torrent_info = make_dict_from_torrent(torrent)
		torrents.append(torrent_info)		
	return torrents

	
