from tracker import Tracker
from peer_manager import PeerManager
from tracker import Tracker
from piece_manager import PieceManager
from block import State
import multiprocessing,time,messages

class Installation_MNG(multiprocessing.Process):
    def __init__(imng,torrent,to_head):
        multiprocessing.Process.__init__(imng)
        #Инициализация трекера
        imng.torrent = torrent
        #Pipe c head
        imng.to_head = to_head
        imng.progress = 0
        

    #Переопределение метода run в Process
    def run(imng):
        imng.initialize_tracker_and_managers()
        imng.display_progress()
 
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
            time.sleep(0.01)
            imng.peer_mng.update_peers()
            imng.display_progress()
        

        imng.display_progress(status = 'Finished')
        imng.close()

    def display_progress(imng,status = 'Downloading'):
        update_progression = 0
        for i in range(imng.piece_mng.number_of_pieces):
            for j in range(imng.piece_mng.pieces[i].number_of_blocks):
                if imng.piece_mng.pieces[i].blocks[j].state == State.FULL:
                    update_progression += len(imng.piece_mng.pieces[i].blocks[j].data)
        
        number_of_active_peers = imng.peer_mng.count_unchoked_peers()
        number_of_inactive_peers = len(imng.peer_mng.peers) - number_of_active_peers
        percentage_completed = round(float((float(update_progression)/imng.torrent.length) * 100),2)

        imng.to_head.send((str(percentage_completed)+"%",status,f'{number_of_active_peers}({number_of_inactive_peers})'))


    def initialize_tracker_and_managers(imng):
        imng.torrent.init_files()
        imng.tracker = Tracker(imng.torrent)
        imng.piece_mng = PieceManager(imng.torrent)
        imng.peer_mng = PeerManager(imng.tracker,imng.piece_mng)
        imng.tracker.get_on_well_with_peer_mng(imng.peer_mng)
        imng.tracker.connect_with_trackers()
        imng.tracker.start()
        
        
        