from tracker import Tracker
from peer_manager import PeerManager
from tracker import Tracker
import multiprocessing

class Installation_MNG(multiprocessing.Process):
    def __init__(imng,torrent):
        multiprocessing.Process.__init__(imng)
        #Инициализация трекера
        imng.tracker = Tracker(torrent)

    #Переопределение метода run в Process
    def run(imng):
        imng.initialize_tracker_connection()
        
    
    def initialize_tracker_connection(imng):
        #Инициализация менеджера пиров
        imng.peer_mng = PeerManager(imng.tracker)
        imng.peer_mng.add_peers()
        