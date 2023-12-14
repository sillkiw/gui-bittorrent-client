from tracker import Tracker
from peer_manager import PeerManager
from tracker import Tracker
from piece_manager import PieceManager
import multiprocessing,time,messages

class Installation_MNG(multiprocessing.Process):
    def __init__(imng,torrent,to_head):
        multiprocessing.Process.__init__(imng)
        #Инициализация трекера
        imng.torrent = torrent
        imng.tracker = Tracker(torrent)
        #Pipe c head
        imng.to_head = to_head

    #Переопределение метода run в Process
    def run(imng):

        imng.torrent.init_files()
        imng.piece_mng = PieceManager(imng.torrent)

        imng.initialize_tracker_and_peer_manager()
        imng.peer_mng.get_on_well_piece_mng(imng.piece_mng)
        imng.peer_mng.start()

        imng.to_head.send(imng.tracker.amount_of_connected_peers)

        while not imng.piece_mng.all_pieces_full():
            if not imng.peer_mng.has_unchoked_peers():
                time.sleep(2)
                print("Все пиры задушены =(")
                continue
            for piece in imng.piece_mng.pieces:
                index = piece.piece_index

                if imng.piece_mng.pieces[index].is_full:
                    continue
                
                peer = imng.peer_mng.get_peer_having_piece(index)
                if not peer:
                    continue

                block_data = imng.piece_mng.pieces[index].get_block_from_free()
                if not block_data:
                    continue

                piece_index,block_offset,block_length = block_data  
                request_msg = messages.request_msg_to_bytes(piece_index,block_offset,block_length)
                peer.sent_message(request_msg)
                print(f"Отправление сообщение Request на блок части с индексом {piece_index} к {peer.ip}")

            time.sleep(0.1)    



    def initialize_tracker_and_peer_manager(imng):
        imng.tracker.connect_with_tracker()
        imng.peer_mng = PeerManager(imng.tracker)
        #Инициализация менеджера пиров
        imng.peer_mng.handshake_with_peers()
        
        