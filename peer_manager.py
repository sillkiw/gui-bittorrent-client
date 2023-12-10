from messages import handshake_msg_to_bytes
from threading import Thread
import select

class PeerManager(Thread):
    def __init__(pmg,tracker):
        Thread.__init__(pmg)
        pmg.tracker = tracker
        pmg.peers = []
        pmg.handshake_message = handshake_msg_to_bytes(pmg.tracker.peer_id,pmg.tracker.info_hash)

    def add_peers(pmg):
        for peer in pmg.tracker.connected_peers:
            if pmg.handshake(peer):
                pmg.peers.append(peer)
            else: 
                print(f"Can't handshake with {peer.ip}")

    def run(pmg):
        while True:
            for peer in pmg.peers:
                try:
                    payload = pmg.read_from_socket(peer.socket)
                except Exception as e:
                    print("Нет ответа от пира "+e.__str__)
                    pmg.remove_peer(peer)
                    continue 
                
                peer.read_buffer += payload
                
                for message in peer.unpack_messages():
                    pmg.answer_new_messages(message,peer)
             
    def remove_peer(pmg,peer):
        try:
            peer.socket.close()
        except Exception:
            pass
        pmg.peers.remove(peer)

    def read_from_socket(pmg,sock):
        data = b''
        while True:
            try:
                ans = sock.recv(4096)
                if len(ans) <= 0:
                    break
                data += ans
            except Exception as e:
                print("error")
                break
        return data

    def handshake(pmg,peer):
        try:
            peer.sent_message(pmg.handshake_message)
            print(f"HandShake with {peer.ip}")
            return True
        except Exception as e:
            print(f"Handshake error with {peer.ip}")