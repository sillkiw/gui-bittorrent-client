from tracker import Tracker
from peer_manager import PeerManager
from tracker import Tracker
import threading

class Installation_MNG(threading.Thread):
    def __init__(imng,head):
        threading.Thread.__init__(imng)
        imng.head = head
        #Инициализация трекера
        imng.tracker = Tracker(head.torrent)

    #Переопределение метода run в Process
    def run(imng):
        imng.initialize_tracker_connection()
        
    
    def initialize_tracker_connection(imng):
        #Подключение к трекеру(отправка ему запроса), и получение списка пиров
        imng.tracker.connect_with_tracker()
        #Инициализация менеджера пиров
        imng.peer_mng = PeerManager(imng.tracker)
        imng.peer_mng.add_peers()
        