PIECE_SIZE = 20#(bytes) размер каждой части определен однозначно 


class Piece:
    def __init__(pie,piece_index,piece_size,piece_hash):
        pie.piece_index = piece_index
        pie.piece_size = piece_size 
        pie.piece_hash = piece_hash
        pie.related_files = []
        pie.is_full = False