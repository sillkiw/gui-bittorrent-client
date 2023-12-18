from messages import handshake_msg_to_bytes
from threading import Thread
import messages
from random import choice
class PeerManager():
    def __init__(pmg,tracker,piece_mng):
        pmg.tracker = tracker
        pmg.peers = []
        pmg.handshake_message = handshake_msg_to_bytes(pmg.tracker.peer_id,pmg.tracker.info_hash)
        pmg.peer_thread = {}
        pmg.piece_mng = piece_mng
    

    def handshake(pmg,peer):
        try:
            peer.sent_message(pmg.handshake_message)
            print(f"Отправка сообщения HandShake к {peer.ip}")
            return True
        except Exception as e:
            return False

    def handshake_with_peer(pmg,peer):
        if pmg.handshake(peer):
            pmg.peers.append(peer)
            hash = peer.__hash__()
            pmg.peer_thread[hash] = Thread(target=pmg.start_to_listen,args=(peer,))
            pmg.peer_thread[hash].start()
        else: 
            print(f"Не получилось отправить сообщение Handshake к {peer.ip}")
            pmg.remove_peer(peer)

    
    def start_to_listen(pmg,peer):
        while True:
                try:
                    payload = pmg.read_from_socket(peer.socket)
                except Exception as e:
                    pmg.remove_peer(peer)
                    continue 
                
                peer.answer_from_me += payload
            
                for message in peer.unpack_messages():
                    pmg.answer_new_messages(message,peer)

    def answer_new_messages(pmg,message,peer):
        message_id = message["id"]
        if message_id == messages.CHOKE_MESSAGE_ID:
            peer.handle_choke()
        elif message_id == messages.UNCHOKE_MESSAGE_ID:
            peer.handle_unchoke()
        elif message_id == messages.INTERESTED_MESSAGE_ID:
            peer.handle_interested()
        elif message_id == messages.NOTINTERESTED_MESSAGE_ID:
            peer.handle_not_interested()
        elif message_id == messages.HAVE_MESSAGE_ID:
            peer.handle_have(message)
        elif message_id == messages.BITFIELD_MESSAGE_ID:
            peer.handle_bitfield(message)
        elif message_id == messages.REQUEST_MESSAGE_ID:
            peer.handle_request(message)
        elif message_id == messages.PIECE_MESSAGE_ID:
            print(f"Получение сообщения 'Piece' от {peer.ip}")
            pmg.piece_mng.handle_piece(message)
        elif message_id == messages.CANCEL_MESSAGE_ID:
            peer.handle_cancel()
        elif message_id == messages.PORT_MESSAGE_ID:
            peer.handle_port()
        else:
            print("Ошибка! Неизвестное сообщение")


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
                break
        return data

    def count_unchoked_peers(pmg):
        count = 0
        for peer in pmg.peers:
            if peer.is_unchoked:
                count += 1
        return count

    def handshake(pmg,peer):
        try:
            peer.sent_message(pmg.handshake_message)
            print(f"HandShake с {peer.ip}")
            return True
        except Exception as e:
            print(f"Handshake error with {peer.ip}")
    
    def get_peer_having_piece(pmg,index):
        exact_peers = [] 
        for peer in pmg.peers:
            if peer.is_open() and  peer.is_unchoked() and peer.am_interested() and peer.has_piece(index):
                exact_peers.append(peer)
        return choice(exact_peers) if exact_peers else None
    
    def has_unchoked_peers(pmg):
        for peer in pmg.peers:
            if peer.is_unchoked():
                return True
        return False
    
    def get_on_well_piece_mng(pmg,piece_mng):
        pmg.piece_mng = piece_mng