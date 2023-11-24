import bencode as ben   #Библиотека для бенкодирования(используется в метафайлах торрента)
import hashlib as hash
import random
import requests as rq
import ipaddress as ip
class Torrent:
    SINGLE_FILE = 1
    MULTIPLE_FILE = 0
    def __init__(tr,file_path):
        tr.torrent_path = file_path
    def read_Metafile(tr) :
        with open(tr.torrent_path,"rb") as torrent_file:
            tr.metainfo = ben.bdecode(torrent_file.read())
            tr.meta_keys = tr.metainfo.keys()

            tr.announce = tr.metainfo['announce']
            tr.info = tr.metainfo['info']
            tr.piece_length = tr.info['piece length']
            tr.piecies = tr.info['pieces']
            tr.name = tr.info['name']
            if 'files' in tr.metainfo['info']:
                tr.files = tr.info['files']
                tr.kind_file = Torrent.MULTIPLE_FILE
            else:
                tr.length = tr.info['length']
                tr.piecies = tr.info['pieces'] #!!!
                tr.kind_file = Torrent.SINGLE_FILE
            tr.prepare_request_GET()
    def prepare_request_GET(tr):
        tr.info_hash = hash.sha1(ben.bencode(tr.info)).digest()
        tr.params = {
            'info_hash':  tr.info_hash,
            'peer_id' : '-PR7070-'+"".join([str(random.randint(0,9)) for _ in range(12)]),
            'port' : 6889,
            'uploaded' : 0,
            'downloaded' : 0,
            'left' : tr.length,
            'event' : 'started'

        }
    def make_request_GET(tr):
        tr.tracker_response = rq.get(tr.announce,params = tr.params)
        print(tr.tracker_response.content)
        print(tr.tracker_response.request)
        a = ben.bdecode(tr.tracker_response.content)
        wor = a['peers']
        print(wor[0])
        print(len(wor))
        
           
           