import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import font
from torrent import Torrent
from hurry.filesize import size
from hurry.filesize import alternative
from enum import Enum
from treelib import Node,Tree
from copy import deepcopy
import os


class winfoWindow(tk.Toplevel):
    
    #Состояния ответа пользователя
    class __States_of_answer__(Enum):
        (T_CLOSED,T_OPENED,U_THINKING) = range(0,3)

    #Окно обзорщика торрент файла
    def __init__(winfo,head):
        super().__init__(head)
    
        winfo.title("Torrent File System ")
        winfo.iconbitmap("images/icon.ico")

        #Ширина всплывающего окна
        winfo.winfo_width = head.head_width // 2 - head.head_width//13
        #Высота всплывающего окна
        winfo.winfo_height = head.head_height - head.head_height//3 - head.head_height//12 
        
        #Центрирование по центру главного окна(head)
        winfo.geometry(f"{winfo.winfo_width}x{winfo.winfo_height}+{(head.sc_width-winfo.winfo_width)//2}+{(head.sc_height-winfo.winfo_height-50)//2}")

        #Инициализация объекта "Torrent"
        winfo.target_torrent = head.target_torrent
        winfo.initialize_torrent()
        
        #Установка стиля
        winfo.set_style()

        #Установка кнопки и лейбла "Source"
        winfo.set_source_label_and_button()
        
        #Установка кнопки и лейбла "Direction"
        winfo.set_destination_label_and_button()

        #Установка обзорщика файловой системы торрент-файла
        winfo.set_file_system()
      
        #Установка кнопок Open и Close
        winfo.set_answer_or_close_frame()
    
        #Не дает пользователю пользоваться главным экраном
        winfo.grab_set()
     
    def initialize_torrent(winfo):
        '''Инициализация торрент-файла'''

        #Путь до торрент файла, выбранного пользователем
        winfo.torrent_path = winfo.target_torrent.name

        #Создание торрента
        winfo.torrent = Torrent(winfo.torrent_path)

    def set_style(winfo):
        '''Установка стиля'''
        winfo.winfo_font = font.Font(family= "Helvetica", size=11) 
        winfo.style_button = ttk.Style()
        winfo.style_button.configure('Heading.TButton', anchor=tk.W,font = winfo.winfo_font)        
    
    def set_source_label_and_button(winfo):
        '''Установка  лейбла Source и кнопки для изменения торрент-файла'''

        winfo.source_frame = tk.Frame(winfo)
        winfo.source_frame.pack(fill=tk.X,pady=20)

        tk.Label(winfo.source_frame,text="Source:",font=winfo.winfo_font).pack(side="left",anchor="w",padx = 18)
       
        #Фото пиратского флага
        winfo.pirate_photo = tk.PhotoImage(file=r"images/icon.png")
        winfo.pirate_photo = winfo.pirate_photo.subsample(3,3)
        
        #Установка кнопки для изменения торрент-файла
        winfo.source_button = ttk.Button(winfo.source_frame,text = " "+winfo.torrent.name,width = winfo.winfo_width//13,image=winfo.pirate_photo,compound="left",style="Heading.TButton",command=winfo.change_torrent)
        winfo.source_button.pack(anchor="sw",padx=26)
    
    def set_destination_label_and_button(winfo):
        '''Установка лейбла Destination и кнопки для изменения места куда будет скачан файл'''
        
        winfo.destination_frame = tk.Frame(winfo)
        winfo.destination_frame.pack(fill=tk.X)

        tk.Label(winfo.destination_frame,text="Destination:",font=winfo.winfo_font).pack(side="left",anchor="w",padx = 18)

        #Иконка файла
        winfo.file_photo = tk.PhotoImage(file=r"images/file_icon.png")
        winfo.file_photo = winfo.file_photo.subsample(5,8)

        #Установка кнопки для изменения пути куда будет скачан файл
        winfo.destination_button = ttk.Button(winfo.destination_frame,text = winfo.torrent.destination,width = winfo.winfo_width//13,image=winfo.file_photo,compound="left",style='Heading.TButton',command=winfo.change_destination)
        winfo.destination_button.pack(anchor="sw")

    def change_torrent(winfo):
        '''Изменение торрент-файла'''
        #Пользователь выбирает новый торрент
        winfo.target_torrent = fd.askopenfile(parent = winfo,initialdir=winfo.torrent.source,filetypes =[('Torrent Files', '*.torrent')]) 

        if winfo.target_torrent:
            #Инициализация нового торрента
            winfo.initialize_torrent()
            
            #Изменение значения на кнопке
            winfo.source_button.config(text = ""+winfo.torrent.name)

            #Удаление файловой системы предыдущего торрента
            for file in winfo.file_system.get_children():
                winfo.file_system.delete(file)

            #Установка файловой системы нового торрента
            winfo.fill_with_torrent_metainfo()

    def change_destination(winfo):
        '''Изменение места установки торрент-файла'''

        #Пользователь выбирает новый путь
        target_destination = fd.askdirectory(parent=winfo,initialdir=winfo.torrent.destination)

        if target_destination:
            #Изменение пути установки в торрент файле
            winfo.torrent.destination = target_destination
            
            #Изменения значения на кнопке
            winfo.destination_button.config(text=winfo.torrent.destination)

    def set_file_system(winfo):
        '''Установка файловой системы'''

        #Фрейм для Treeview
        winfo.file_system_frame = ttk.Frame(winfo)
        winfo.file_system_frame.pack(pady=10)

        #Скролбар
        winfo.vsb = ttk.Scrollbar(winfo.file_system_frame)
        winfo.vsb.pack(side = tk.RIGHT,fill=tk.Y)

        #Установка файловой системы
        winfo.file_system = ttk.Treeview(winfo.file_system_frame,yscrollcommand=winfo.vsb.set)
        winfo.set_columns_and_fill_headings()
        winfo.fill_with_torrent_metainfo()

        winfo.vsb.config(command=winfo.file_system.yview)
        winfo.file_system.pack() 


    #Установка столбцов и строк для файловой системы
    def set_columns_and_fill_headings(winfo):
        '''Установка столбцов и заполнение заголовков'''
        winfo.file_system['columns'] = ('Size')

        winfo.file_system.column("#0",anchor='w',width=winfo.winfo_width//2+winfo.winfo_width//6)
        winfo.file_system.column('Size',anchor='center',width=winfo.winfo_width//4)

        winfo.file_system.heading("#0",text="Name",anchor="w")
        winfo.file_system.heading('Size',text = 'Size',anchor = "w")
 
    def fill_with_torrent_metainfo(winfo):  
        '''Заполнение обзорщика файловой системы файлами, которые указаны в метаданных торрент-файла'''
        
        #Чтение метафайла
        winfo.torrent.read_Metafile()
        
        #Проверка файловой системы торрент-файла
        if winfo.torrent.kind_file == Torrent._Kinds_of_file.SINGLE_FILE:
            winfo.file_system.insert(parent="",index = "end",text= winfo.torrent.file_name,values = [winfo.torrent.size])  
        
        elif winfo.torrent.kind_file == Torrent._Kinds_of_file.MULTIPLE_FILE:
           winfo.magic()
        
    def magic(winfo):        
        name_and_size = {}
        all = deepcopy(winfo.torrent.files2)
        file_table = create_file_system(winfo.torrent.file_name,winfo.torrent.length,all,name_and_size)
        file_table = file_table.to_dict()
        children = file_table[winfo.torrent.file_name]['children']
        id = {"folder":1,"file":-1}
        winfo.file_system.insert('','end',text = winfo.torrent.file_name,iid = id["folder"],values=[convert(name_and_size[winfo.torrent.file_name])],open=True)
        id['folder']+=1
        for file in children:
            if isinstance(file,dict):
                name = list(file.keys())[0]
                children = file[name]['children']
                winfo.file_system.insert('','end',text = name,iid = id["folder"],values=[convert(name_and_size[name])])
                winfo.file_system.move(id["folder"],1,1000000)
                id["folder"] += 1
                winfo.cont(children,id,name_and_size)
            else:
                winfo.file_system.insert('','end',text = file,iid = id["file"],values=[convert(name_and_size[file])])
                winfo.file_system.move(id["file"],1,1000000)
                id["file"] -= 1      
    def cont(winfo,children,id,name_and_size):
        for child in children:
            if isinstance(child,dict):
                name = list(children_next.keys())[0]
                children_next = child[name]['children']
                winfo.file_system.insert('','end',iid  = id["folder"],text = name,values=[convert(name_and_size[name])])
                winfo.file_system.move(id["folder"],id["folder"]-1,10000)
                id["folder"] += 1
                winfo.cont(children_next,id,name_and_size)
            else:
                    winfo.file_system.insert('','end',iid = id["file"],text = child,values=[convert(name_and_size[child])])
                    winfo.file_system.move(id["file"],id["folder"]-1,1000000)
                    id["file"] -= 1

    def set_answer_or_close_frame(winfo):
        '''Установка двух кнопок Open | Close''' 
        
        #Состояние ответа
        winfo.state_of_answer = winfoWindow.__States_of_answer__.U_THINKING
        
        answer_frame = tk.Frame(winfo)
        answer_frame.pack(fill=tk.X)
        
        #Кнопка Close
        winfo.button_Close = ttk.Button(answer_frame,text = "Close",width = winfo.winfo_width//40,command = winfo.close_pressed)
        winfo.button_Close.pack(side = tk.RIGHT,anchor="ce",padx=27)
        
        #Кнопка Open
        winfo.button_Open =  ttk.Button(answer_frame,text = "Open",width = winfo.winfo_width//40,command = winfo.open_pressed)
        winfo.button_Open.pack(anchor="e")
     
    
    def close_pressed(winfo):
        '''Ответ на событие нажатия кнопки Close'''
        
        #Пользователь отказался от установки
        winfo.state_of_answer = winfoWindow.__States_of_answer__.T_CLOSED
        
        #Разрещаем пользователю пользоваться главным окном
        winfo.grab_release()

        #Закрытие информационного окна
        winfo.destroy()

    def open_pressed(winfo):
        '''Ответ на событие нажатия кнопки Open'''

        #Пользователь согласился на установку
        winfo.state_of_answer = winfoWindow.__States_of_answer__.T_OPENED
           
        #Разрещаем пользователю пользоваться главным окном
        winfo.grab_release()

        #Закрытие информационного окна
        winfo.destroy()


def convert(siz):
    return size(siz,system=alternative)

def create_file_system(dir_name,dir_size,files,name_and_size):
    file_system = Tree()
    root = file_system.create_node(dir_name,dir_name)
    name_and_size[dir_name] = dir_size
    for file in files:
        path = file['path']
        size = file['length']
        len_of_path = len(path)
        if len_of_path > 1:
            name_of_folder = path.pop(0)
            if name_of_folder in name_and_size.keys():
                name_and_size[name_of_folder] += size
                folder  = file_system.get_node(name_of_folder)
            else:
                name_and_size[name_of_folder] = size
                folder = file_system.create_node(name_of_folder,name_of_folder,parent=root)
            file_system = untill_file(path,size,folder,len_of_path-1,name_and_size,file_system)
        else:
            file_name = path[0]
            file_system.create_node(file_name,parent=root,data=size)
            name_and_size[file_name] = size
    return file_system

def untill_file(path,size,folder,len_of_path,name_and_size,file_system):
    if len_of_path == 1:
        name = path.pop(0)
        name_and_size[name] = size
        file_system.create_node(name,name,parent=folder)
        return file_system
    else:
        name = path.pop(0)
        if name in name_and_size.keys():
            name_and_size[name] += size
        else:
            name_and_size[name] = size
        nfolder = file_system.create_node(name,name,parent=folder)
        untill_file(path,size,nfolder,len_of_path-1,name_and_size)