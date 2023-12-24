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
from pathlib import Path
from random import randint



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
        winfo.winfo_font = font.Font(family= "Helvetica", size=13) 
        winfo.winfo_font2 = font.Font(family= "Helvetica", size=15) 
        winfo.style_button = ttk.Style()
        winfo.style_button.configure('Heading.TButton', anchor=tk.W,font = winfo.winfo_font)        
        winfo.style_button.configure('Heading.Label', anchor=tk.W,font = winfo.winfo_font2)    
    
    def set_source_label_and_button(winfo):
        '''Установка  лейбла Source и кнопки для изменения торрент-файла'''

        winfo.source_frame = tk.Frame(winfo)
        winfo.source_frame.pack(fill=tk.X,pady=20)

        ttk.Label(winfo.source_frame,text="Source:",width=11,font=winfo.winfo_font,style='Heading.Label').pack(side="left",anchor="w")
       
        #Фото пиратского флага
        winfo.pirate_photo = tk.PhotoImage(file=r"images/icon.png")
        winfo.pirate_photo = winfo.pirate_photo.subsample(3,3)
        
        #Установка кнопки для изменения торрент-файла
        winfo.source_button = ttk.Button(winfo.source_frame,text = " "+winfo.torrent.name,width = winfo.winfo_width//13,image=winfo.pirate_photo,compound="left",style="Heading.TButton",command=winfo.change_torrent)
        winfo.source_button.pack(anchor="sw")
    
    def set_destination_label_and_button(winfo):
        '''Установка лейбла Destination и кнопки для изменения места куда будет скачан файл'''
        
        winfo.destination_frame = tk.Frame(winfo)
        winfo.destination_frame.pack(fill=tk.X)

        ttk.Label(winfo.destination_frame,width=10,text="Destination:",font=winfo.winfo_font).pack(side="left",anchor="w")

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

        winfo.tick_image = tk.PhotoImage(file=r"images/tick.png")
        winfo.not_tick_image = tk.PhotoImage(file=r"images/not_tick.png") 

        #Установка файловой системы
        winfo.file_system = ttk.Treeview(winfo.file_system_frame,yscrollcommand=winfo.vsb.set,style="mystyle.Treeview")

        winfo.file_system.tag_configure('chose',image=winfo.tick_image)
        winfo.file_system.tag_configure('unchose',image=winfo.not_tick_image)

        winfo.bind("<Button-1>", winfo.box_click, True)

        winfo.set_columns_and_fill_headings()
        winfo.fill_with_torrent_metainfo()

        winfo.vsb.config(command=winfo.file_system.yview)
        winfo.file_system.pack() 

    def box_click(winfo, event):
        """ check or uncheck box when clicked """
        try:
            x, y, widget = event.x, event.y, event.widget
            elem = widget.identify("element", x, y)
            
            if "image" in elem:
                # a box was clicked
                item = winfo.file_system.identify_row(y)
                tags = winfo.file_system.item(item, "tags")
                if ("unchose" in tags):
                    winfo.check_ancestor(item)
                    winfo.check_descendant(item)
                else:
                    winfo.uncheck_descendant(item)
                    winfo.uncheck_ancestor(item)
        except Exception:
            pass

    def check_descendant(winfo, item):
        """ check the boxes of item's descendants """
        children = winfo.file_system.get_children(item)
        for iid in children:
            winfo.file_system.item(iid, tags=("chose",))
            winfo.check_descendant(iid)

    def check_ancestor(winfo, item):
        """ check the box of item and change the state of the boxes of item's
            ancestors accordingly """
        winfo.file_system.item(item, tags=("chose",))
        parent = winfo.file_system.parent(item)
        if parent:        
            winfo.check_parent(parent)
            winfo.check_ancestor(parent)

    def uncheck_descendant(winfo, item):
        """ uncheck the boxes of item's descendant """
        children = winfo.file_system.get_children(item)
        for iid in children:
            winfo.file_system.item(iid, tags=("unchose",))
            winfo.uncheck_descendant(iid)
    
    def check_parent(winfo, item):
        """ put the box of item in tristate and change the state of the boxes of
            item's ancestors accordingly """
        winfo.file_system.item(item, tags=("chose",))
        parent = winfo.file_system.parent(item)
        if parent:
            winfo.check_parent(parent)
    
    def uncheck_parent(winfo, item):
        winfo.file_system.item(item, tags=("unchose",))
        print(parent)
        parent = winfo.file_system.parent(item)
        if parent:
            children = winfo.file_system.get_children(parent)
            b = ["unchose" in winfo.file_system.item(c, "tags") for c in children]
            if all(b):
                winfo.uncheck_parent(parent)

    def uncheck_ancestor(winfo, item):
        """ uncheck the box of item and change the state of the boxes of item's
            ancestors accordingly """
        winfo.file_system.item(item, tags=("unchose",))
        parent = winfo.file_system.parent(item)
        if parent:
            children = winfo.file_system.get_children(parent)
            b = ["unchose" in winfo.file_system.item(c, "tags") for c in children]
            if all(b):
                winfo.uncheck_parent(parent)
            # else:
            #     # no box is chose
            #     winfo.uncheck_ancestor(parent)

    #Установка столбцов и строк для файловой системы
    def set_columns_and_fill_headings(winfo):
        '''Установка столбцов и заполнение заголовков'''
        winfo.file_system['columns'] = ('Size')

        winfo.file_system.column("#0",anchor='w',width=winfo.winfo_width//2+winfo.winfo_width//5)
        winfo.file_system.column('Size',anchor='center',width=winfo.winfo_width//6)

        winfo.file_system.heading("#0",text="Name",anchor="w")
        winfo.file_system.heading('Size',text = 'Size',anchor = "w")
 
    def fill_with_torrent_metainfo(winfo):  
        '''Заполнение обзорщика файловой системы файлами, которые указаны в метаданных торрент-файла'''
        #Чтение метафайла
        winfo.torrent.read_Metafile()
        
        #Инициализация файловой системы, указанной в метаданных торрент-файла
        winfo.torrent.init_files()

        #Отображение на экране
        winfo.create_dict_from_paths()
        winfo.show_in_file_system()

        

    def create_dict_from_paths(winfo):
        def _recurse(dic, chain):
            if len(chain) == 0:
                return
            if len(chain) == 1:
                dic[chain[0]] = None
                return
            key, *new_chain = chain
            if key not in dic:
                dic[key] = {}
            _recurse(dic[key], new_chain)
            return
        winfo.file_dict = {}
        for file in winfo.torrent.file_names:
            _recurse(winfo.file_dict, Path(file['path']).parts)

    def insert_to_treeview(winfo,name):
        winfo.file_system.insert('','end',text =name, iid = name,values=[winfo.torrent.size],open=True,tags='chose')
    
    def insert_to_root_folder(winfo,name,folder,size = 0):
        try:
            winfo.file_system.insert(folder,'end',text =name, iid = name,values=[size],open=False,tags='chose')
        except Exception:
            name_to_iid = name+f'{randint(0,10000)}'
            winfo.file_system.insert(folder,'end',text =name, iid = name_to_iid,values=[size],open=False,tags='chose')
            name = name_to_iid
        return name
    
    def show_in_file_system(winfo):
        def _recur(root_folder,root_folder_name):
            for file_or_folder_name in root_folder:
                inside = root_folder[file_or_folder_name]
     
                if isinstance(inside,dict):
                    new_folder_name = file_or_folder_name
                    new_folder_name = winfo.insert_to_root_folder(file_or_folder_name,root_folder_name)
                    
                    winfo.folder_sizes[new_folder_name] = 0
                    
                    _recur(inside,new_folder_name)
                    
                    winfo.folder_sizes[root_folder_name] += winfo.folder_sizes[new_folder_name]
                else:
                    new_file_name = file_or_folder_name
                    file_size = winfo.torrent.file_his_size[new_file_name]
                    
                    winfo.insert_to_root_folder(new_file_name,root_folder_name,size = convert(file_size))
                    
                    winfo.folder_sizes[root_folder_name] += file_size
         
        root_folder_name = winfo.torrent.root_folder_name
        file_system_in_root = winfo.file_dict[root_folder_name]
        
        winfo.insert_to_treeview(root_folder_name)
        
        winfo.folder_sizes = {}

        winfo.folder_sizes[root_folder_name] = 0

        _recur(file_system_in_root,root_folder_name)

        winfo.put_sizes_to_folder_in_treeview()
    
    def put_sizes_to_folder_in_treeview(winfo):
        for folder in winfo.folder_sizes:
            winfo.file_system.item(folder,values=[convert(winfo.folder_sizes[folder])])


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

