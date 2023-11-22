import bencode as ben   #Библиотека для бенкодирования(используется в метафайлах торрента)


class Torrent:
    def __init__(meta,file_path):
        meta.torrent_path = file_path
    def open_and_read_Metafile(meta) :
        with open(meta.torrent_path,"rb") as torrent_file:
            meta.metainfo = ben.bdecode(torrent_file.read())
            meta.info = meta.metainfo['info']


            print(type(meta.info))
            print(meta.info)
           