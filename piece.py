import math,time,hashlib
from block import BLOCK_SIZE,Block,State

PIECE_LEN = 20#(bytes) длина каждой части определен однозначно 


class Piece:
    def __init__(pie,piece_index,piece_size,piece_hash):
        pie.piece_index = piece_index
        pie.piece_size = piece_size
        pie.piece_hash = piece_hash
        pie.related_files = []
        pie.is_full = False
        pie.number_of_blocks = int(math.ceil(float(piece_size)/BLOCK_SIZE))
        pie.init_blocks()


    def init_blocks(pie):
        pie.blocks = []

        if pie.number_of_blocks > 1:
            for i in range(pie.number_of_blocks):
                pie.blocks.append(Block())

            if (pie.piece_size % BLOCK_SIZE) > 0:
                pie.blocks[pie.number_of_blocks-1].block_size = pie.piece_size % BLOCK_SIZE
        else:
            pie.blocks.append(Block(block_size=int(pie.piece_size)))
    
    def put_to_block(pie,offset,data):
        index = int(offset / BLOCK_SIZE)
        
        if not pie.is_full and not pie.blocks[index].state == State.FULL:
            pie.blocks[index].data = data
            pie.blocks[index].state = State.FULL
    
    def relief_piece_from_buff(pie):
        data = pie.merge_blocks()

        if not pie.check_blocks(data):
            pie.init_blocks()
            return False
        pie.is_full = True
        pie.data = data
        pie.put_piece_on_disk()
        return True

    
    def put_piece_on_disk(pie):
        for file in pie.related_files:
            path_file = file['path']
            file_offset = file['fileOffset']
            piece_offset = file['pieceOffset']
            legnth = file['length']

            try:
                f = open(path_file,'r+b')
            except IOError:
                f = open(path_file,'wb')
            except Exception:
                print("Не получается записать файл")
                return
            f.seek(file_offset)
            f.write(pie.data[piece_offset:piece_offset+legnth])
            f.close()




    def merge_blocks(pie):
        buf = b''
        for block in pie.blocks:
            buf += block.data
        return buf
    
    def get_block_from_free(pie):
        if pie.is_full:
            return None
        
        for i in range(0,len(pie.blocks)):
            if pie.blocks[i].state == State.FREE:
                pie.blocks[i].state = State.PEDNING
                pie.blocks[i].last_seen = time.time()
                block_offset = i * BLOCK_SIZE
                return pie.piece_index, block_offset, pie.blocks[i].block_size
    
    def all_blocks_full(pie):
        for block in pie.blocks:
            if block.state == State.FREE or block.state == State.PEDNING:
                return False
        return True
    
    def check_blocks(pie,data):
        hashed_raw_data = hashlib.sha1(data).digest()

        if hashed_raw_data == pie.piece_hash:
            return True
        else:
            print(f"Хеши не совпадают | запись части с индексом {pie.piece_index}")
        return False