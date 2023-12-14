import math
from block import BLOCK_SIZE,Block
PIECE_SIZE = 20#(bytes) размер каждой части определен однозначно 


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