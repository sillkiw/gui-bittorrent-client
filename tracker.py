import hashlib as hash
import bencode as ben
import requests as req
import ipaddress as ipform
import struct
from random import randint
from tkinter import messagebox
from peer import Peer
class Tracker:
        def __init__(track,torrent_file):
            track.url = torrent_file.announce
            track.info_hash = hash.sha1(ben.bencode(torrent_file.info)).digest()
            track.peer_id = b'-PR7070-'+bytes([randint(0,9) for _ in range(12)])
            track.user_port = 6881
            track.amount_uploaded = 0
            track.amount_downloaded = 0
            track.left = torrent_file.length
            track.connected_peers = []
        def connect_with_tracker(track):
            track.parametrs = { #параметры для верного подключения
                'info_hash' : track.info_hash,
                'peer_id' : track.peer_id,
                'port' : track.user_port,
                'uploaded' : track.amount_uploaded,
                'downloaded' : track.amount_downloaded,
                'left' :  track.left,
                'event' : 'started'
            }
            try:
                track.response = req.get(track.url,track.parametrs)
                track.response = ben.bdecode(track.response.content)
            except Exception:
                 messagebox.showerror("Can't connect with a tracker")
        def get_list_of_peers(track):
            track.packed_peers = track.response['peers']
            track.amount_of_peers = len(track.packed_peers) // 6
            track.list_of_peers = []
            track.big_endian_unpack()   
            
        def big_endian_unpack(track):
             position = 0
             for _ in range(track.amount_of_peers):
                peer_ip = struct.unpack_from("!i", track.packed_peers,offset=position)[0]
                peer_ip = ipform.IPv4Address(struct.pack("!i",peer_ip))
                
                position += 4
                peer_port = struct.unpack_from("!H",track.packed_peers,position)[0]

                position += 2
                
                track.list_of_peers.append(Peer(peer_ip,peer_port))
        
        def connect_with_peers(track):
            
            for peer in track.list_of_peers:
                if not peer.connect():
                    continue
                print(f"CONNECTED WITH {peer.ip}")
                track.connected_peers.append(peer)   
            print(track.connected_peers)
        def make_messages(track):
            track.HANDSHAKE = b"\x13Bittorent protocol"+track.info_hash+track.peer_id        