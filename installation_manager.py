from tracker import Tracker
from peer_manager import PeerManager
from tracker import Tracker
from piece_manager import PieceManager
import multiprocessing

class Installation_MNG(multiprocessing.Process):
    def __init__(imng,torrent,to_head):
        multiprocessing.Process.__init__(imng)
        #Инициализация трекера
        imng.torrent = torrent
        imng.torrent.init_files()
        imng.tracker = Tracker(torrent)
        imng.piece_mng = PieceManager(torrent)
       
        #Pipe c head
        imng.to_head = to_head

    #Переопределение метода run в Process
    def run(imng):
        imng.initialize_tracker_and_peer_manager()
        imng.to_head.send(imng.tracker.amount_of_connected_peers)
        
    def initialize_tracker_and_peer_manager(imng):
        imng.tracker.connect_with_tracker()
        imng.peer_mng = PeerManager(imng.tracker)
        #Инициализация менеджера пиров
        imng.peer_mng.handshake_with_peers()
        imng.peer_mng.start()
        