import hashlib as hash
import bencode as ben
import requests as req
from random import randint
from tkinter import messagebox
from peer import Peer
import struct,socket,time
class Tracker:      
        def __init__(track,torrent):
            track.url = torrent.announce
            track.info_hash = hash.sha1(ben.bencode(torrent.info)).digest()
            track.peer_id = b'-PR7070-'+bytes([randint(0,9) for _ in range(12)])
            track.user_port = 6881
            track.amount_uploaded = 0
            track.amount_downloaded = 0
            track.left = torrent.length
            track.connected_peers = []
            track.torrent = torrent

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
                track.packed_peers = track.response['peers']
                track.interval = track.response['interval']
                track.connect_with_peers()
            except Exception:
                # TODO Остановить процесс!!!
                 messagebox.showerror("Erorr","Can't connect with a tracker")
                 
        def connect_with_peers(track):
            track.get_list_of_peers()
            track.amount_of_peers = len(track.list_of_peers)
            for peer in track.list_of_peers:
                if not peer.connect():
                    continue
                print(f"CONNECTED WITH {peer.ip}")
                track.connected_peers.append(peer)   
            track.amount_of_connected_peers = len(track.connected_peers)

        def get_list_of_peers(track):
            track.packed_peers = track.response['peers']
            track.amount_of_peers = len(track.packed_peers) // 6
            track.list_of_peers = []
            track.big_endian_unpack()   
            
        def big_endian_unpack(track):
             position = 0
             for _ in range(track.amount_of_peers):
                peer_ip = struct.unpack_from("!i", track.packed_peers,offset=position)[0]
                peer_ip = socket.inet_ntoa(struct.pack("!i",peer_ip))     
                position += 4
                peer_port = struct.unpack_from("!H",track.packed_peers,position)[0]
                position += 2
                track.list_of_peers.append(Peer(peer_ip,peer_port,track))
        
 