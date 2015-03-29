import re
import inspect
import urllib
import requests
import json
import utils


base_url = {'t411' : 'http://api.t411.me', 'torrent-hunter' : 'http://localhost:81/api/v1'}

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
	torrent_info['title'] = torrent['title']
	torrent_info["size"] = torrent['size']
	torrent_info["id"] = torrent["tracker"] + '_' + torrent['slug']
	torrent_info["seeders"] = torrent['seeds']
	torrent_info["leechers"] = torrent['leechs']
	return torrent_info

def make_dict_from_torrent_t411(torrent):	
	torrent_info = {}
	torrent_info["title"] = torrent["name"]
	torrent_info["size"] = sizeof_fmt(float(torrent["size"]))
	torrent_info["id"] = torrent["id"]
	torrent_info["seeders"] = torrent['seeders']
	torrent_info["leechers"] = torrent['leechers']
	return torrent_info

def get_torrents_by_query(tracker, query, offset, authorization):
	torrents = []
	if tracker == 't411':
		search_url = base_url['t411'] + '/torrents/search/' + query + '&offset=' + str(offset) + '&limit=30'
	else:
		search_url = base_url['torrent-hunter'] + '/search?query=' + query + '&offset=' + str(offset) + '&limit=30'

	result_req = requests.get(search_url, headers={'Authorization': authorization})
	print result_req.text
	for torrent in json.loads(result_req.text)["torrents"]:
		torrent_info = make_dict_from_torrent_t411(torrent) if tracker == 't411' else make_dict_from_torrent(torrent)
		torrents.append(torrent_info)
	return torrents

def get_tops(tracker, authorization):
	torrents = []
	if tracker == 't411':
		search_url = base_url['t411'] + '/torrents/top/100'
	else:
		search_url = base_url['torrent-hunter'] + '/torrents/top'
	result_req = requests.get(search_url, headers={'Authorization': authorization})
	print search_url
	for torrent in json.loads(result_req.text):		
		torrent_info = make_dict_from_torrent_t411(torrent) if tracker == 't411' else make_dict_from_torrent(torrent)		
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
	torrent_info['description'] = json.loads(result_req.text)["description"]
	return torrent_info

def get_torrent_info_torrent_hunter(torrent_id):		
	torrent_info = {}
	id = torrent_id.split("_")
	r = requests.get(base_url['torrent-hunter'] + "/torrent/" + id[0] + "/details/" + id[1])
	return json.loads(r.text)["details"]

def get_torrent_file_t411(id, authorization):
	r = requests.get('http://api.t411.me/torrents/download/' + id,  headers={'Authorization': authorization})
	return {'magnet_link': utils.createMagnetLinkFromTorrent(r.content)}

def get_torrent_file_torrent_hunter(tracker_provider, slug):
	r = requests.get(base_url['torrent-hunter'] + '/torrent/' + tracker_provider + '/' + slug)
	return {'magnet_link': json.loads(r.text)['downloadLink']}

