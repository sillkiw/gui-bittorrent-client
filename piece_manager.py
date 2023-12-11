from bitstring import BitArray
import piece

class PieceManager:
    def __init__(piemng,torrent):
        piemng.torrent = torrent
        piemng.number_of_pieces = torrent.number_of_pieces
        piemng.bitfield = BitArray(piemng.number_of_pieces)
        piemng.initialize_pieces()
    
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