from tracker import Tracker
from peer_manager import PeerManager
from tracker import Tracker
from piece_manager import PieceManager
from block import State
from hurry.filesize import size,alternative
import multiprocessing,time,messages

class Installation_MNG(multiprocessing.Process):
    def __init__(imng,torrent,to_head):
        multiprocessing.Process.__init__(imng)
        #Инициализация трекера
        imng.torrent = torrent
        #Pipe c head
        imng.to_head = to_head
        #Общий прогресс установки
        imng.progress = 0
        imng.progress_in_per = 0
        imng.sum_installation = 0
        imng.sum_time = 0

    #Переопределение метода run в Process
    def run(imng):
        imng.initialize_tracker_and_managers()
        imng.display_progress(status='Initializing...')
        imng.time1 = time.time()
        while not imng.piece_mng.all_pieces_full():
            if not imng.peer_mng.has_unchoked_peers():
                time.sleep(2)
                print("Все пиры задушены =(")
                continue
            
            for piece in imng.piece_mng.pieces:
                index = piece.piece_index

                if imng.piece_mng.pieces[index].is_full:
                    continue
                    
                imng.piece_mng.pieces[index].update_block_status()

                peer = imng.peer_mng.get_peer_having_piece(index)
                if not peer:
                    continue

                block_data = imng.piece_mng.pieces[index].get_block_from_free()
                if not block_data:
                    continue

                piece_index,block_offset,block_length = block_data  
                request_msg = messages.request_msg_to_bytes(piece_index,block_offset,block_length)
                if peer.sent_message(request_msg):
                    peer.requets_message_sent += 1

            #imng.peer_mng.check_peers()
            time.sleep(0.2)
            imng.time2 = time.time()
            imng.display_progress()
            if imng.progress_in_per % 10 == 0 and imng.progress_in_per:
                imng.peer_mng.check_peers()


        

        imng.display_progress(status = 'Finished')
        imng.close()

    def display_progress(imng,status = 'Downloading...'):
        update_progression = 0
        
        for piece in imng.piece_mng.pieces:
            for block in piece.blocks:
                if block.state == State.FULL:
                    update_progression += len(block.data)
        
        if status == 'Initializing...':
            imng.speed = "∞"
        elif status == 'Finished':
            imng.speed = ''
        elif update_progression != imng.progress:
            imng.sum_installation += update_progression
            imng.sum_time += imng.time2 - imng.time1
            imng.speed = round(imng.sum_installation/imng.sum_time,2)
            imng.speed = size(imng.speed,system=alternative)
        
        number_of_active_peers = imng.peer_mng.count_unchoked_peers()
        number_of_inactive_peers = len(imng.peer_mng.peers) - number_of_active_peers
        imng.progress = update_progression
        imng.progress_in_per = round(float((float(imng.progress)/imng.torrent.length) * 100),2)
    
        imng.to_head.send((str(imng.progress_in_per)+"%",status,f'{number_of_active_peers}({number_of_inactive_peers})',f'{imng.speed}/s'))


    def initialize_tracker_and_managers(imng):
        imng.torrent.init_files()
        imng.tracker = Tracker(imng.torrent)
        imng.piece_mng = PieceManager(imng.torrent)
        imng.peer_mng = PeerManager(imng.tracker,imng.piece_mng)
        imng.tracker.get_on_well_with_peer_mng(imng.peer_mng)
        imng.tracker.connect_with_trackers()
        imng.tracker.start()
        
        
        