from installation_manager import Installation_MNG
from multiprocessing import Pipe,Value
import threading,os
from enum import Enum
from hurry.filesize import size,alternative
#Установочная форма
class InstallationForm:
   
    RUN,STOP,DELETE,FINISHED = range(0,4)

    def __init__(install_form,head,torrent,id,size):
        install_form.head = head
        install_form.name,_ = os.path.splitext(torrent.name)
        install_form.size = size
        install_form.size_c = convert(install_form.size)
        install_form.id = id
        install_form.status = Value('i',InstallationForm.RUN)
        #Труба для обмена сообщениями между установочным процессорои и графическим интерфейсом
        install_form.to_head,install_form.from_install = Pipe()
        #Установочный процесс
        install_form.installation_mng = Installation_MNG(torrent,install_form.to_head,install_form.status,install_form.size)
        #Поток для изменения информации на экране
        install_form.updater_thread = threading.Thread(target=install_form.updater,daemon=True)
    
    #Размещение установочной формы на экран
    def pack_to_viewer(install_form):
        install_form.head.viewer.insert(parent="",index = "end",iid = install_form.id,
                           values = (install_form.name,install_form.size_c,"0.0%","Initializing...","0(0)","∞"),tags = ('tor')) 
        
    #Обновление установочной формы
    def updater(install_form):
        while install_form.status.value != InstallationForm.FINISHED and install_form.status.value != InstallationForm.DELETE:
            try:
                #Получение информации от установки
                progress,status,peers,speed = install_form.from_install.recv()
                #Изменение информации об установки
                install_form.head.viewer.item(install_form.id,values=(install_form.name,install_form.size_c,progress,status,peers,speed))
            except Exception:
                continue

    def begin(install_form):
        #Запустить поток обновляющий информацию на GUI
        install_form.updater_thread.start()
        #Запустить процесс начала установки
        install_form.installation_mng.start()

def convert(siz):
    return size(siz,system=alternative)
