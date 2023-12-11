

class PieceManager:
    def __init__(piemng,torrent):
        piemng.torrent = torrent
        piemng.number_of_pieces = torrent.number_of_pieces