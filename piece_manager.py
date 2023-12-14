from bitstring import BitArray
import piece

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
            piemng.pieces[id_piece].related_files.append(file)
    
    def initialize_pieces(piemng):
        piemng.pieces = []
        #индекс последней части
        index_of_last_pie = piemng.number_of_pieces - 1

        for pie_index in range(piemng.number_of_pieces):
            start = pie_index*piece.PIECE_SIZE
            end = start+piece.PIECE_SIZE

            #последняя часть имеет не фиксированный размер
            if pie_index == index_of_last_pie:
                last_pie_length = piemng.torrent.length - (piemng.number_of_pieces) * piemng.torrent.piece_length
                piemng.pieces.append(piece.Piece(pie_index,last_pie_length,piemng.torrent.pieces[start:end]))
            else:
                piemng.pieces.append(piece.Piece(pie_index,piemng.torrent.piece_length,piemng.torrent.pieces[start:end])) 
    
    def all_pieces_full(piemng):
        for piece in piemng.pieces:
            if not piece.is_full:
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
                            "path": f["path"]
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
                            "path": f["path"]
                            }
                    piece_offset += piece_size
                    file_offset += piece_size
                    piece_size_used = 0

                piemng.files.append(file)
               
