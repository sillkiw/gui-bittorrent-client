from bitstring import BitArray
from piece import Piece,PIECE_LEN

class PieceManager:
    def __init__(piemng,torrent):
        piemng.torrent = torrent
        piemng.number_of_pieces = torrent.number_of_pieces
        piemng.bitfield = BitArray(piemng.number_of_pieces)
        piemng.initialize_pieces()
        piemng.complete_pieces = 0
        piemng._load_files()
        for file in piemng.files:
            id_piece = file['idPiece']
            if file['download']:
                piemng.pieces[id_piece].to_download = True
            piemng.pieces[id_piece].related_files.append(file)
    
    def initialize_pieces(piemng):
        piemng.pieces = []
        #индекс последней части
        index_of_last_pie = piemng.number_of_pieces - 1

        for pie_index in range(piemng.number_of_pieces):
            start = pie_index*PIECE_LEN
            end = start+PIECE_LEN

            #последняя часть имеет не фиксированный размер, определенный в метафайле
            if pie_index == index_of_last_pie:
                last_pie_length = piemng.torrent.length - (piemng.number_of_pieces-1) * piemng.torrent.piece_length
                piemng.pieces.append(Piece(pie_index,last_pie_length,piemng.torrent.pieces[start:end]))
            else:
                piemng.pieces.append(Piece(pie_index,piemng.torrent.piece_length,piemng.torrent.pieces[start:end])) 
    
    def handle_piece(piemng,piece_message):
        piece_index = piece_message['piece_index']
        block_offset = piece_message['begin']
        block_data = piece_message['block']
 
        if piemng.pieces[piece_index].is_full:
            return
        try:
            piemng.pieces[piece_index].put_to_block(block_offset,block_data)
            
            if piemng.pieces[piece_index].all_blocks_full():
                if piemng.pieces[piece_index].relief_piece_from_buff():
                    piemng.bitfield[piece_index] = 1
                    piemng.complete_pieces += 1
        except Exception:
            return False
        
        return True

 

    def all_pieces_full(piemng):
        for piece in piemng.pieces:
            if not piece.is_full and piece.to_download:
                return False
        return True

    def _load_files(piemng):
        piemng.files = []
        piece_offset = 0
        piece_size_used = 0

        for f in piemng.torrent.file_names:
            current_size_file = f["length"]
            file_offset = 0

            while current_size_file > 0:
                id_piece = int(piece_offset / piemng.torrent.piece_length)
                piece_size = piemng.pieces[id_piece].piece_size - piece_size_used

                if current_size_file - piece_size < 0:
                    file = {"length": current_size_file,
                            "idPiece": id_piece,
                            "fileOffset": file_offset,
                            "pieceOffset": piece_size_used,
                            "path": f["path"],
                            "download" : f['chose']
                            }
                    piece_offset += current_size_file
                    file_offset += current_size_file
                    piece_size_used += current_size_file
                    current_size_file = 0

                else:
                    current_size_file -= piece_size
                    file = {"length": piece_size,
                            "idPiece": id_piece,
                            "fileOffset": file_offset,
                            "pieceOffset": piece_size_used,
                            "path": f["path"],
                            "download" : f['chose']
                            }
                    piece_offset += piece_size
                    file_offset += piece_size
                    piece_size_used = 0

                piemng.files.append(file)
               
