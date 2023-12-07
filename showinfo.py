import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import font
from torrent import Torrent
from hurry.filesize import size
from hurry.filesize import alternative

class winfoWindow(tk.Toplevel):
    #Состояния ответа пользователя
    class _States_of_answer:
        T_CLOSED,U_THINKING,T_OPENED = (-1,0,1)
    #Окно обзорщика торрент файла
    def __init__(winfo,head):
         super().__init__(head)
         winfo.title("Torrent File System ")
         winfo.iconbitmap("images/icon.ico")
        #Размеры всплывающего окна
         winfo.winfo_width = head.head_width // 3 #Ширина всплывающего окна
         winfo.winfo_height = head.head_height // 2  + head.head_height//25 #Высота всплывающего окна
        #Центрирование по центру главного окна(head)
         winfo.geometry(f"{winfo.winfo_width}x{winfo.winfo_height}+{(head.head_width-winfo.winfo_width)//2}+{(head.head_height-winfo.winfo_height)//2}")
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
        #Обзорщик файловой системы торрента
         winfo.file_system = ttk.Treeview(winfo,show="headings")
         winfo.set_file_system()
        #Инициализация торрента в виде объкта
         winfo.torrent = Torrent(winfo.torrent_path,winfo.torrent_name)
         winfo.fill_the_table()
         winfo.file_system.pack(pady = 10) 
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
        winfo.file_system['columns'] = ("File","Type","Size")
        #Инициализация столбцов
        winfo.file_system.column("#0")
        winfo.file_system.column("File",anchor = "w",width=200,minwidth = 200)
        winfo.file_system.column("Type",anchor="w",width=70,minwidth = 70)
        winfo.file_system.column("Size",anchor="w",width=120,minwidth=120)
        #Инициализация строк
        winfo.file_system.heading("#0")
        winfo.file_system.heading("File",text="File",anchor="w")
        winfo.file_system.heading("Type",text="Type",anchor="w")
        winfo.file_system.heading("Size",text="Size",anchor="w")
    
    #Заполнение обзорщика файла файлами торрента
    def fill_the_table(winfo):  
        #Чтение метафайла
        winfo.torrent.read_Metafile()
        #Проверка типа файла 
        if winfo.torrent.kind_file == Torrent._Kinds_of_file.SINGLE_FILE:
            #Имя одного файла
            name_of_one_file = winfo.torrent.info['name']
            #Разделение на имя и на тип файла
            winfo.name,winfo.type = dividePrefix(name_of_one_file,".")
            #Общий размер = размер одного файла
            winfo.size = winfo.torrent.size
            #Вставка в обзорщик файловой системы
            winfo.file_system.insert(parent="",index = "end",values = (winfo.name,"."+winfo.type,winfo.size))
        elif winfo.torrent.kind_file == Torrent._Kinds_of_file.MULTIPLE_FILE:
            pass


#Вспомогательная функция для разделения префикса 
def dividePrefix(path,sym):
    parts  = path.split(sym)
    last_part = parts.pop(-1)
    prefix_part =  sym.join(parts)
    return prefix_part,last_part