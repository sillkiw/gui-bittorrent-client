import hashlib as hash
import bencode as ben
import requests as req
from random import randint
from tkinter import messagebox
from peer import Peer
from messages import upd_tracker_connection_form_message
import struct,socket,time


MAX_PEER_CONNECTED = 10
MAX_PEER_TRY_CONNECT = 30

class Tracker:      
        def __init__(track,torrent):
            track.url = torrent.announce
            track.info_hash = hash.sha1(ben.bencode(torrent.info)).digest()
            track.peer_id = b'-PR7070-'+bytes([randint(0,9) for _ in range(12)])
            track.user_port = 6881
            track.left = torrent.length
            track.connected_peers = []
            track.torrent = torrent
            track.announce_list = torrent.announce_list
            track.list_of_peers_form = []

        def connect_with_trackers(track):  
            for tracker in track.announce_list:

                if str.startswith(tracker,"http"):
                    try:
                        tracker.http_handle()
                    except Exception as e:
                        print(f"Не получается подключиться к трекеру {tracker}")
                elif str.startswith(tracker,"udp"):
                    try:
                        tracker.udp_handle()
                    except Exception as e:
                        print(f"Не получается подключиться к трекеру {tracker}")
                else:
                    pass
            track.connect_with_peers
        def http_handle(track):
            track.parametrs = {
                'info_hash' : track.info_hash,
                'peer_id' : track.peer_id,
                'uploaded' : 0,
                'downloaded' : 0,
                'port' : track.user_port,
                'left' : track.left,
                'event' : 'started'
             }
            try:
                response = req.get(track.url,track.parametrs)
                response = ben.bdecode(track.response.content)
                peers_data = track.response['peers']
                if isinstance(peers_data,list):
                    list_of_peer_forms = track.big_endian_unpack_for_http_response(peers_data)
                    track.list_of_peers_form.append(*list_of_peer_forms)
                else:
                    for peer_data in peers_data:
                        peer_form= [peer_data['ip'],peer_data['port']]
                        track.list_of_peers_form.append(peer_form)
                
            except Exception:
                # TODO Остановить процесс!!!
                 messagebox.showerror("Erorr","Can't connect with a tracker")
                   
        def big_endian_unpack_for_http_response(track,peers_data):
             list_of_forms = []
             amount_of_peer_data = len(peers_data)//6
             for _ in range(amount_of_peer_data):
                peer_ip = struct.unpack_from("!i", peers_data,offset=position)[0]
                peer_ip = socket.inet_ntoa(struct.pack("!i",peer_ip))     
                position += 4

                peer_port = struct.unpack_from("!H",peers_data.packed_peers,position)[0]
                position += 2
                
                list_of_forms.append([peer_ip,peer_port])
        
        


        #def udp_handle(track):
            
            

        def connect_with_peers(track):
            track.get_list_of_peers()
            track.amount_of_peers = len(track.list_of_peers)
            for peer_form in track.list_of_peers:
                if not peer.connect():
                    continue
                print(f"CONNECTED WITH {peer.ip}")
                track.connected_peers.append(peer)   
            track.amount_of_connected_peers = len(track.connected_peers)

 
        
 