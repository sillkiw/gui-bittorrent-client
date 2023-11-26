import bencode as ben   #Библиотека для бенкодирования(используется в метафайлах торрента)
import hashlib as hash
import random
import requests as rq
import ipaddress as ip
import socket
import struct

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
                tr.length = 0
                for file in tr.files:
                    tr.length += file['length']
            else:
                tr.length = tr.info['length']
                tr.piecies = tr.info['pieces'] #!!!
                tr.kind_file = Torrent.SINGLE_FILE
            tr.prepare_request_GET()
  
    def prepare_request_GET(tr):
        tr.info_hash = hash.sha1(ben.bencode(tr.info)).digest()
        tr.peer_id = b'-PR7070-'+bytes([random.randint(0,9) for _ in range(12)])
        tr.params = {
            'info_hash':  tr.info_hash,
            'peer_id' : tr.peer_id,
            'port' : 6881,
            'uploaded' : 0,
            'downloaded' : 0,
            'left' : tr.length,
            'event' : 'started'

        }
    def make_request_GET(tr):

        tr.tracker_response = rq.get(tr.announce,params = tr.params)
    def connect_with_peer(tr):
      
      
        tr.resp_content = ben.bdecode(tr.tracker_response.content)
        tr.list_peers = tr.resp_content['peers']
        tr.make_clean()
        print(tr.ls)
        tr.handshake = b"\x13Bittorent Protocol\0\0\0\0\0\0\0\0"+tr.info_hash+tr.peer_id
        print(len(tr.h))
        tr.sock = socket.create_connection((tr.ls[1][0],tr.ls[1][1]),timeout=2)
        tr.sock.send(tr.handshake)
        
        buff = tr.sock.recv(len(tr.handshake))
        
       

    def make_clean(tr):
          tr.ls = []
          offset = 0
          for _ in range(len(tr.list_peers)//6):
                    ip = struct.unpack_from("!i", tr.list_peers, offset)[0]
                    ip = socket.inet_ntoa(struct.pack("!i", ip))
                    offset += 4
                    port = struct.unpack_from("!H",tr.list_peers, offset)[0]
                    offset += 2
                    tr.ls.append([ip,port])
                    
           