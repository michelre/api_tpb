import sys
import urllib
import bencode
import hashlib
import base64

def createMagnetLinkFromTorrent(torrent):
	metadata = bencode.bdecode(torrent)

	hashcontents = bencode.bencode(metadata['info'])	
	digest = hashlib.sha1(hashcontents).digest()	
	b32hash = base64.b32encode(digest)

	params = 'dn=' + urllib.quote_plus(metadata['info']['name']) + '&xt=' + 'urn:btih:%s' % b32hash
	announcestr = '&tr=' + urllib.quote_plus(metadata['announce'])

	paramstr = params + announcestr
	magneturi = 'magnet:?%s' % paramstr
	return magneturi