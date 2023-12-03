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
         winfo.winfo_width = head.head_width // 3 #Ширина окна
         winfo.winfo_height = head.head_height // 2  + head.head_height//30 #Высота окна
        #Центрирование по центру главного окна(head)
         winfo.geometry(f"{winfo.winfo_width}x{winfo.winfo_height}+{(head.head_width-winfo.winfo_width)//2}+{(head.head_height-winfo.winfo_height)//2}")
        #Путь до файла выбранного пользователя 
         winfo.file_path = head.target_file.name
         winfo.file_dir,winfo.torrent_name = dividePrefix(winfo.file_path,"/")
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
        #Графа для выбора файла, в которой будет помещен торрент
         winfo.file_frame = tk.Frame(winfo)
         winfo.file_frame.pack(fill=tk.X)
         tk.Label(winfo.file_frame,text="Destination:",font=winfo.winfo_font).pack(side="left",anchor="w",padx = 20)
        #Кнопка
         winfo.file_photo = tk.PhotoImage(file=r"images/file_icon.png")
         winfo.file_photo = winfo.file_photo.subsample(5,8)
         winfo.file_button = ttk.Button(winfo.file_frame,text = winfo.file_dir,width = winfo.winfo_width//13,image=winfo.file_photo,compound="left",style='Heading.TButton',command=winfo.change_destination)
         winfo.file_button.pack(anchor="sw",padx=20)
        #Файловая система
         winfo.file_system = ttk.Treeview(winfo,show="headings")
         winfo.set_file_system()
        #Открытия торрент-файла и чтение метафайла
         winfo.torrent = Torrent(winfo.file_path,winfo.torrent_name)
         winfo.fill_the_table()
         winfo.file_system.pack(pady = 10) 
        #Ответ пользователя
         winfo.state_of_answer = winfoWindow._States_of_answer.U_THINKING
         winfo.answer_frame = tk.Frame(winfo)
         winfo.answer_frame.pack(fill=tk.X)
         winfo.button_Close = ttk.Button(winfo.answer_frame,text = "Close",width = winfo.winfo_width//40,command = winfo.close_window)
         winfo.button_Close.pack(side = tk.RIGHT,anchor="ce",padx=27)
         winfo.button_Open =  ttk.Button(winfo.answer_frame,text = "Open",width = winfo.winfo_width//40,command = winfo.mark_torrent_open)
         winfo.button_Open.pack(anchor="e")
         winfo.grab_set()
     
       
     
    def close_window(winfo):
        winfo.state_of_answer = winfoWindow._States_of_answer.T_CLOSED
        winfo.grab_release()
        winfo.destroy()


    def mark_torrent_open(winfo):
        winfo.state_of_answer = winfoWindow._States_of_answer.T_OPENED
        winfo.grab_release()
        winfo.destroy()
    
    #Изменение торрента
    def change_torrent(winfo):
        target_file = fd.askopenfile(parent = winfo,initialdir=winfo.file_dir,filetypes =[('Torrent Files', '*.torrent')]) 
        winfo.file_path = target_file.name
        winfo.torrent_name = winfo.file_path.split("/")[-1]
        winfo.source_button.config(text = winfo.torrent_name)
        winfo.torrent = Torrent(winfo.file_path,winfo.torrent_name)
        for file in winfo.file_system.get_children():
            winfo.file_system.delete(file)

        winfo.fill_the_table()


    #Изменение места установки торрент-файла
    def change_destination(winfo):
        target_destination = fd.askdirectory(parent=winfo,initialdir=winfo.file_dir)
        winfo.file_dir = target_destination
        winfo.file_button.config(text=winfo.file_dir)


    #Установка столбцов для файловой системы
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
    
    def fill_the_table(winfo):  
        winfo.torrent.read_Metafile()
        if  winfo.torrent.kind_file == Torrent._Kinds_of_file.SINGLE_FILE:
            winfo.n_ame,winfo.t_ype = dividePrefix(winfo.torrent.info['name'],".")
            winfo.t_ype="."+winfo.t_ype
            winfo.s_ize = size(winfo.torrent.info['length'],system=alternative)
            winfo.file_system.insert(parent="",index = "end",iid=0,values = (winfo.n_ame,winfo.t_ype,winfo.s_ize))



#Вспомогательная функция вне класса 
def dividePrefix(path,sym):
    parts  = path.split(sym)
    last_part = parts.pop(-1)
    prefix_part =  sym.join(parts)
    return prefix_part,last_part