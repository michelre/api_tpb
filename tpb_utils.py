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

def find_sub_categories(path, acc):	
	if inspect.isclass(eval(path)):
		for name in dir(eval(path)):		
			if not name.startswith('_'):
				acc[-1]["categories"].append({"name": name, "categories":[]})
				find_sub_categories(path+'.'+name, acc[-1]["categories"])
	return acc

def get_categories():
	return find_sub_categories('CATEGORIES', [{"name": "CATEGORIES", "categories": []}])

def get_torrents_per_category(category):
	torrents = []
	for torrent in t.top().category(eval(category)):
		torrent_info = make_dict_from_torrent(torrent)
		torrents.append(torrent_info)		
	return torrents

	
