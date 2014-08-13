from tpb import TPB
from tpb import CATEGORIES, ORDERS

t = TPB('https://thepiratebay.org') # create a TPB object with default domain

def get_torrents_by_query(query, offset):
	torrents = []
	#result = {}
	
	for torrent in t.search(query).order(ORDERS.SEEDERS.DES).page(offset):
		torrent_info = {}
		torrent_info["title"] = torrent.title
		torrent_info["size"] = torrent.size
		torrent_info["download_link"] = torrent.magnet_link
		torrent_info["seeders"] = torrent.seeders
		torrents.append(torrent_info)
	#result["result"] = torrents
	return torrents
