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
    class _States_of_answer(Enum):
        T_CLOSED = -1 #Окно закрыли
        U_THINKING = 0 #Окно работает
        T_OPENED = 1 #Пользователь нажал на open

    #Окно обзорщика торрент файла
    def __init__(winfo,head):
         super().__init__(head)
         winfo.title("Torrent File System ")
         winfo.iconbitmap("images/icon.ico")
        #Размеры всплывающего окна
         winfo.winfo_width = head.head_width // 3 #Ширина всплывающего окна
         winfo.winfo_height = head.head_height - head.head_height//3 - head.head_height//12 #Высота всплывающего окна
        #Центрирование по центру главного окна(head)
         winfo.geometry(f"{winfo.winfo_width}x{winfo.winfo_height}+{(head.sc_width-winfo.winfo_width)//2}+{(head.sc_height-winfo.winfo_height-50)//2}")
        #Путь до торрент-файла выбранного пользователя 
         winfo.torrent_path = head.target_torrent.name
         winfo.direction,winfo.torrent_name = dividePrefix(winfo.torrent_path,"/")
        #Стиль для кнопки и шрифта
         winfo.winfo_font = font.Font(family= "Segoe UI", size=10) 
         winfo.style_button = ttk.Style()
         winfo.style_button.configure('Heading.TButton', anchor=tk.W,font = winfo.winfo_font)
        #Графа для изменения торрент-файла
         winfo.source_frame = tk.Frame(winfo)
         winfo.source_frame.pack(fill=tk.X)
         tk.Label(winfo.source_frame,text="Torrent sourse:",font=winfo.winfo_font).pack(side="left",anchor="w",padx = 20,pady=20)
        #Кнопка для изменения торрент-файла в окне обзорщика торрента
         winfo.source_photo = tk.PhotoImage(file=r"images/icon.png")
         winfo.source_photo = winfo.source_photo.subsample(3,3)
         winfo.source_button = ttk.Button(winfo.source_frame,text = winfo.torrent_name,width = winfo.winfo_width//13,image=winfo.source_photo,compound="left",style="Heading.TButton",command=winfo.change_torrent)
         winfo.source_button.pack(anchor="sw",pady=20,ipadx=1)
        #Графа для выбора пути, в которой будет помещен скачанный торрент
         winfo.file_frame = tk.Frame(winfo)
         winfo.file_frame.pack(fill=tk.X)
         tk.Label(winfo.file_frame,text="Destination:",font=winfo.winfo_font).pack(side="left",anchor="w",padx = 20)
        #Кнопка для выбора пути, в которой будет помещен скачанный торрент
         winfo.file_photo = tk.PhotoImage(file=r"images/file_icon.png")
         winfo.file_photo = winfo.file_photo.subsample(5,8)
         winfo.file_button = ttk.Button(winfo.file_frame,text = winfo.direction,width = winfo.winfo_width//13,image=winfo.file_photo,compound="left",style='Heading.TButton',command=winfo.change_destination)
         winfo.file_button.pack(anchor="sw",padx=20)
         winfo.torrent = Torrent(winfo.torrent_path,winfo.torrent_name)
        #Обзорщик файловой системы торрента
         winfo.file_system_frame = ttk.Frame(winfo)
         winfo.file_system_frame.pack(pady=10)
         winfo.vsb = ttk.Scrollbar(winfo.file_system_frame)
         winfo.vsb.pack(side = tk.RIGHT,fill=tk.Y)
         winfo.file_system = ttk.Treeview(winfo.file_system_frame,yscrollcommand=winfo.vsb.set)
         winfo.set_file_system()
         winfo.fill_the_table()
         winfo.vsb.config(command=winfo.file_system.yview)
         winfo.file_system.pack() 
        #Пользователь еще ничего не нажал
         winfo.state_of_answer = winfoWindow._States_of_answer.U_THINKING
         winfo.answer_frame = tk.Frame(winfo)
         winfo.answer_frame.pack(fill=tk.X)
        #Кнопка закрытия 
         winfo.button_Close = ttk.Button(winfo.answer_frame,text = "Close",width = winfo.winfo_width//40,command = winfo.close_pressed)
         winfo.button_Close.pack(side = tk.RIGHT,anchor="ce",padx=27)
        #Кнопка согласия на скачку торрента
         winfo.button_Open =  ttk.Button(winfo.answer_frame,text = "Open",width = winfo.winfo_width//40,command = winfo.open_pressed)
         winfo.button_Open.pack(anchor="e")
        #Запрет пользователю пользоваться главным окном
         winfo.grab_set()
     
       
    #Пользователь нажал Close
    def close_pressed(winfo):
        #Пользователь отказался от установки
        winfo.state_of_answer = winfoWindow._States_of_answer.T_CLOSED
        #Закрытие окна
        winfo.grab_release()
        winfo.destroy()

    #Пользователь нажал Open
    def open_pressed(winfo):
        #Пользователь согласился на установку
        winfo.state_of_answer = winfoWindow._States_of_answer.T_OPENED
        #Закрытие окна
        winfo.torrent.init_files(winfo.direction)
        winfo.grab_release()
        winfo.destroy()
    
   
            
           
    
    #Изменение торрент-файла
    def change_torrent(winfo):
        #Пользователь выбирает новый торрент
        new_target_torrent = fd.askopenfile(parent = winfo,initialdir=winfo.direction,filetypes =[('Torrent Files', '*.torrent')]) 
        #Изменение всех предыдущих значений
        winfo.torrent_path = new_target_torrent.name
        winfo.direction,winfo.torrent_name = dividePrefix(winfo.torrent_path,"/")
        winfo.source_button.config(text = winfo.torrent_name)
        winfo.torrent = Torrent(winfo.torrent_path,winfo.torrent_name)
        #Удаление файловой системы предыдущего торрента
        for file in winfo.file_system.get_children():
            winfo.file_system.delete(file)
        #Установка файловой системы нового торрента
        winfo.fill_the_table()


    #Изменение места установки торрент-файла
    def change_destination(winfo):
        #Пользователь выбирает новый путь
        target_destination = fd.askdirectory(parent=winfo,initialdir=winfo.direction)
        #Изменение предыдущих значений
        winfo.direction = target_destination
        winfo.file_button.config(text=winfo.direction)


    #Установка столбцов и строк для файловой системы
    def set_file_system(winfo):
        winfo.file_system['columns'] = ('Size')
        winfo.file_system.column("#0",anchor='w',width=winfo.winfo_width//2+winfo.winfo_width//5)
        winfo.file_system.column('Size',anchor='center',width=winfo.winfo_width//6)
        winfo.file_system.heading("#0",text="Name",anchor="w")
        winfo.file_system.heading('Size',text = 'Size',anchor = "w")

            
    
        
    #Заполнение обзорщика файла файлами торрента
    def fill_the_table(winfo):  
        #Чтение метафайла
        winfo.torrent.read_Metafile()
        #Проверка типа файла 
        if winfo.torrent.kind_file == Torrent._Kinds_of_file.SINGLE_FILE:
            #Имя одного файла
            name_of_one_file = winfo.torrent.file_name
            #Разделение на имя и на тип файла
            #Общий размер = размер одного файла
            winfo.size = winfo.torrent.size
            #Вставка в обзорщик файловой системы
            r = winfo.size
            winfo.file_system.insert(parent="",index = "end",text= name_of_one_file,values = [r])
        elif winfo.torrent.kind_file == Torrent._Kinds_of_file.MULTIPLE_FILE:
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
                    

        
#Вспомогательная функция для разделения префикса 
def dividePrefix(path,sym):
    parts  = path.split(sym)
    last_part = parts.pop(-1)
    prefix_part =  sym.join(parts)
    return prefix_part,last_part

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
            if name_of_folder == '[Sotark] Naruto Shippuden [480p][720p][HEVC][x265][Dual-Audio]':
                print('a)')
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