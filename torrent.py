import bencode as ben,math,os   #Библиотека для бенкодирования(используется в метафайлах торрента)
from hurry.filesize import size,alternative
from enum import Enum


class Torrent: 
    #Типы файла
    class _Kinds_of_file(Enum):
       SINGLE_FILE,MULTIPLE_FILE = (0,1)
     
    
    def __init__(tr,file_path):
        #Путь до торрента
        tr.torrent_path = file_path
        #Разделение пути и имени торрент-файла
        tr.source,tr.name = tr.split_torrent_path()
        #Путь места, куда будет установлен торрент-файл
        tr.destination = tr.source #Первоначально файл будет установлен там, где пользователь его выбрал
        #Словарь с файлами 
        tr.file_names = []
       
        
    #Чтение метаданных с метафайла
    def read_Metafile(tr):
        #Открытие торрент-файла
        with open(tr.torrent_path,"rb") as torrent_file:
            #Чтение файла и декодирование бенкода
            tr.metainfo = ben.bdecode(torrent_file.read())
            
            #url-адресс трекера
            tr.announce_list = tr.get_trackers()
            
            #info - информация о файлах торрента, частях 
            tr.info = tr.metainfo['info']
            
            #piece length - размер одной части 
            tr.piece_length = tr.info['piece length']
            #pieces - SHA1 хеши частей файла \ файлов
            tr.pieces = tr.info['pieces']
            
            #Если определено несколько файлов в info
            if 'files' in tr.metainfo['info']:
                #Имя главной папки
                tr.file_name = tr.info['name']
                tr.files = tr.info['files']
                tr.files2 = tr.info['files']
                
                #Тип файловой системы
                tr.kind_file = Torrent._Kinds_of_file.MULTIPLE_FILE
                
                #Общий размер
                tr.length = 0
                for file in tr.files:
                    tr.length += file['length']
            else:
                #Имя единственного файла
                tr.file_name = tr.info['name']
                tr.files = None
                
                #Тип файловой системы
                tr.kind_file = Torrent._Kinds_of_file.SINGLE_FILE
                
                #Размер файла
                tr.length = tr.info['length']

            #Рассчет количества частей
            tr.number_of_pieces = math.ceil(tr.length/tr.piece_length)

            #Представление размера файлов в красивом виде    
            tr.size =  size(tr.length,system=alternative)

    def get_trackers(tr):
        if 'announce-list' in tr.metainfo:
            list_of_trackers = tr.metainfo['announce-list']
            list_of_trackers.append([tr.metainfo['announce']])
            return list_of_trackers
        else:
            return [[tr.metainfo['announce']]]

    #Создание файловой системы торрента
    def init_files(tr):
        #Создаем главную папку 
        root = tr.destination+"/"+tr.file_name
        #Проверка типа файловой системы  торрента
        if tr.kind_file == tr._Kinds_of_file.MULTIPLE_FILE:
            #Если такой папки не существует
            #if not os.path.exists(root):
                #Создаем такую папку
             #   os.mkdir(root, 0o0766 )

            #Для каждого файла в info['files']
            for file in tr.files:
                #Присоединение имени файла к root
                path_file = os.path.join(root, *file["path"])

                #Создание такой папки
                #if not os.path.exists(os.path.dirname(path_file)):
                #    os.makedirs(os.path.dirname(path_file))

                #Сохраняем имя файла и его размер
                tr.file_names.append({"path": path_file , "length": file["length"]})
        else:
            #Если файл всего лишь, то сохраняем имя файла и его размер
            tr.file_names.append({"path": root , "length": tr.length})
    

    def split_torrent_path(tr):
        parts  = tr.torrent_path.split("/")
        last_part = parts.pop(-1)
        prefix_part =  '/'.join(parts)
        return prefix_part,last_part
    