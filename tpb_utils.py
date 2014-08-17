from tpb import TPB
from tpb import CATEGORIES, ORDERS
import re

t = TPB('https://thepiratebay.org') # create a TPB object with default domain

def get_torrents_by_query(query, offset):
	torrents = []	
	for torrent in t.search(query).order(ORDERS.SEEDERS.DES).page(offset):
		torrent_info = {}
		torrent_info["title"] = torrent.title
		torrent_info["size"] = torrent.size
		torrent_info["download_link"] = torrent.magnet_link
		torrents.append(torrent_info)
	return torrents

def get_categories():
	categories = []
	for name in dir(CATEGORIES):
		if not name.startswith('_'):			
			attr = getattr(CATEGORIES, name)
			sub_categories = str(attr).split("\n")[1:]
			all_sub_categories = []
			current = {}
			for sub_cat in sub_categories:												
				if sub_cat != '':
					all_sub_categories.append(sub_cat.split(":")[0].strip())
					current[name] = all_sub_categories
			categories.append(current)
	return categories

def get_torrent_top(offset):
	print CATEGORIES
