from tracker import Tracker
from peer_manager import PeerManager
from tracker import Tracker
from piece_manager import PieceManager
import multiprocessing,time

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
        imng.to_head.send(imng.tracker.amount_of_connected_peers)
        
        while not imng.piece_mng.all_pieces_full():
            if not imng.peer_mng.has_unchoked_peers():
                time.sleep(2)
                print("Все пиры задушены =(")
                continue
            for piece in imng.piece_mng.pieces:
                index = piece.piece_index

                if imng.peer_mng.pieces[index].is_full:
                    continue
                
                peer = imng.peer_mng.get_peer_having_piece(index)

                if not peer:
                    continue

                



    def initialize_tracker_and_peer_manager(imng):
        imng.tracker.connect_with_tracker()
        imng.peer_mng = PeerManager(imng.tracker)
        #Инициализация менеджера пиров
        imng.peer_mng.handshake_with_peers()
        imng.peer_mng.start()
        