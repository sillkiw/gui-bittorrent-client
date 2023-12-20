import hashlib as hash
import bencode as ben
import requests as req
from random import randint
from tkinter import messagebox
from urllib.parse import urlparse
from peer import Peer
import struct,socket,time,messages
from peer_manager import PeerManager
from threading import Thread


MAX_PEER_CONNECTED = 25

class Tracker(Thread):      
        
        def __init__(track,torrent):
            Thread.__init__(track)
            track.info_hash = hash.sha1(ben.bencode(torrent.info)).digest()
            track.peer_id = b'-PR7070-'+bytes([randint(0,9) for _ in range(12)])
            track.user_port = 6881
            track.left = torrent.length
            track.connected_peers = []
            track.torrent = torrent
            track.announce_list = torrent.announce_list
            track.list_of_peers_form = []
            track.parametrs_for_http_get = {
                'info_hash' : track.info_hash,
                'peer_id' : track.peer_id,
                'uploaded' : 0,
                'downloaded' : 0,
                'port' : track.user_port,
                'left' : track.left,
                'event' : 'started'
             }
            

        def connect_with_trackers(track):  
            for tracker in track.announce_list:
                url = tracker[0]
                if str.startswith(url,"http"):
                    try:
                        track.http_handle(url)
                    except Exception:
                        print(f"Не удалось отправить запрос к трекеру {url}, либо ответ трекера был неверен")
                elif str.startswith(url,"udp"):
                    try:
                        track.udp_handle(url)
                    except Exception:
                        print(f"Не удалось отправить запрос к трекеру {url}, либо ответ трекера был неверен")
                else:
                    pass
           

        def http_handle(track,url):
            try:
                print(f"Попытка отправить запрос к трекеру {url}")
                response_from_tracker= req.get(url,track.parametrs_for_http_get,timeout=1)
                response_from_tracker = ben.bdecode(response_from_tracker.content)
                print(f"Получение ответа от трекера {url}")
                peers_data = response_from_tracker['peers']
                if isinstance(peers_data,bytes):
                    track.big_endian_unpack(peers_data)
                else:
                    for peer_data in peers_data:
                        peer_form = make_peer_form(peer_data['ip'],peer_data['port'])
                        track.list_of_peers_form.append(peer_form)
               
            except Exception:
                raise Exception()
        
        def udp_handle(track,url):
            parsed = urlparse(url)

            try:
                url_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                url_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                url_socket.settimeout(1)

                ip,port = socket.gethostbyname(parsed.hostname),parsed.port

                tracker_connection_message,trans_id = messages.upd_tracker_connection_form_message()
                conn_id = track.send_message((ip,port),url_socket,tracker_connection_message,
                                            messages.upd_tracker_connection_form_message_recieve,trans_id)

                tracker_announce_message,trans_id = messages.upd_tracker_annnounce_form_message(track.peer_id,track.info_hash,conn_id)

                peers_data = track.send_message((ip,port),url_socket,tracker_announce_message,
                                                messages.upd_tracker_annnounce_form_message_recieve,trans_id)
                
                track.big_endian_unpack(peers_data)
            except Exception:
                raise Exception()


        def send_message(track,tracker_form,sock,message,receiver,trans_id):
            sock.sendto(message,tracker_form)
      
            try:
                response = sock.recv(4096)
            except Exception as e:
                raise Exception()
                
            
            accept,response = receiver(response,trans_id)

            if not accept:
                raise Exception()
            
            return response
            

        def big_endian_unpack(track,peers_data):
            amount_of_peer_data = len(peers_data)//6
            position = 0
            for _ in range(amount_of_peer_data):
               peer_ip = struct.unpack_from("!i", peers_data,offset=position)[0]
               peer_ip = socket.inet_ntoa(struct.pack("!i",peer_ip))     
               position += 4

               peer_port = struct.unpack_from("!H",peers_data,offset=position)[0]
               position += 2
               
               peer_form = make_peer_form(peer_ip,peer_port)
               track.list_of_peers_form.append( peer_form )
   
        
        def run(track):
            for peer_form in track.list_of_peers_form:
                if len(track.connected_peers) > MAX_PEER_CONNECTED:
                    time.sleep(50)
                    continue
                ip = peer_form['ip']
                port = peer_form['port']
                new_peer = Peer(ip,port,track)
                print(f"Попытка подключения к {new_peer.ip}")
                if not new_peer.connect():
                    print(f"Не удалось подключиться к {new_peer.ip}")
                    continue
                print(f"Получилось подключиться к {new_peer.ip}")
                track.peer_mng.handshake_with_peer(new_peer)

                track.connected_peers.append(new_peer)
                time.sleep(15)
            track.amount_of_connected_peers = len(track.connected_peers)

        def get_on_well_with_peer_mng(track,peer_mng):
            track.peer_mng = peer_mng

def make_peer_form(ip,port):
    return {'ip':ip,'port':port}


        