import bencode as ben   #Библиотека для бенкодирования(используется в метафайлах торрента)


class Torrent:
    SINGLE_FILE = 1
    MULTIPLE_FILE = 0
    def __init__(tr,file_path):
        tr.torrent_path = file_path
    def read_Metafile(tr) :
        with open(tr.torrent_path,"rb") as torrent_file:
            tr.metainfo = ben.bdecode(torrent_file.read())
            tr.meta_keys = tr.metainfo.keys()

            tr.announce = tr.metainfo['announce']
            tr.info = tr.metainfo['info']
            tr.piece_length = tr.info['piece length']
            tr.piecies = tr.info['pieces']
            tr.name = tr.info['name']
            if 'files' in tr.metainfo['info']:
                tr.files = tr.info['files']
                tr.kind_file = Torrent.MULTIPLE_FILE
            else:
                tr.length = tr.info['length']
                tr.piecies = tr.info['pieces']
                tr.kind_file = Torrent.SINGLE_FILE

        

           
           