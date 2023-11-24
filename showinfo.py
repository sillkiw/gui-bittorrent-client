import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import font
from torrent import Torrent
from hurry.filesize import size
from hurry.filesize import alternative
class InfoWindow(tk.Toplevel):
    STILL_THINKING = 0
    T_CLOSED = -1
    T_OPENED = 1
    #Окно обзорщика торрент файла
    def __init__(info,head,file_path,head_width,head_height):
         super().__init__(head)
         
         info.title("Torrent File System ")
         info.iconbitmap("images/icon.ico")
         
         info.info_width = head_width // 3 #Ширина окна
         info.info_height = head_height // 2  + head_height//30 #Высота окна

        #Центрирование по центру главного окна(head)
         info.geometry(f"{info.info_width}x{info.info_height}+{(head_width-info.info_width)//2}+{(head_height-info.info_height)//2}")
       
        #Путь до файла выбранного пользователя 
         info.file_path = file_path
         info.file_dir,info.torrent_name = dividePrefix(file_path,"/")
        #Стиль для кнопки и шрифта
         info.info_font = font.Font(family= "Segoe UI", size=10) 
         info.style_button = ttk.Style()
         info.style_button.configure('Heading.TButton', anchor=tk.W,font = info.info_font)
         
         
        #Графа для изменения торрент-файла
         info.source_frame = tk.Frame(info)
         info.source_frame.pack(fill=tk.X)
         tk.Label(info.source_frame,text="Torrent sourse:",font=info.info_font).pack(side="left",anchor="w",padx = 20,pady=20)
        #Кнопка для изменения торрент-файла в окне обзорщика торрента
         info.source_photo = tk.PhotoImage(file=r"images/icon.png")
         info.source_photo = info.source_photo.subsample(3,3)
         info.source_button = ttk.Button(info.source_frame,text = info.torrent_name,width = info.info_width//13,image=info.source_photo,compound="left",style="Heading.TButton",command=info.change_torrent)
         info.source_button.pack(anchor="sw",pady=20,ipadx=1)
         

        #Графа для выбора файла, в которой будет помещен торрент
         info.file_frame = tk.Frame(info)
         info.file_frame.pack(fill=tk.X)
         tk.Label(info.file_frame,text="Destination:",font=info.info_font).pack(side="left",anchor="w",padx = 20)
        #Кнопка
         info.file_photo = tk.PhotoImage(file=r"images/file_icon.png")
         info.file_photo = info.file_photo.subsample(5,8)
         info.file_button = ttk.Button(info.file_frame,text = info.file_dir,width = info.info_width//13,image=info.file_photo,compound="left",style='Heading.TButton',command=info.change_destination)
         info.file_button.pack(anchor="sw",padx=20)


        #Файловая система
         info.file_system = ttk.Treeview(info,show="headings")
         info.set_file_system()
        #Открытия торрент-файла и чтение метафайла
         info.opened_torrent = Torrent(info.file_path)
         info.fill_the_table()

         info.file_system.pack(pady = 10) 
         
        #Ответ пользователя
         info.state_of_answer = InfoWindow.STILL_THINKING

         info.answer_frame = tk.Frame(info)
         info.answer_frame.pack(fill=tk.X)
         info.button_Close = ttk.Button(info.answer_frame,text = "Close",width = info.info_width//40,command = info.close_window)
         info.button_Close.pack(side = tk.RIGHT,anchor="ce",padx=27)
         info.button_Open =  ttk.Button(info.answer_frame,text = "Open",width = info.info_width//40,command = info.mark_torrent_open)
         info.button_Open.pack(anchor="e")
         
         info.grab_set()
     
       
     
    def close_window(info):
        info.state_of_answer = InfoWindow.T_CLOSED
        info.grab_release()
        info.destroy()
    def mark_torrent_open(info):
        info.state_of_answer = InfoWindow.T_OPENED
        info.grab_release()
        info.destroy()
    
    #Изменение торрента
    def change_torrent(info):
        target_file = fd.askopenfile(parent = info,initialdir=info.file_dir,filetypes =[('Torrent Files', '*.torrent')]) 
        info.file_path = target_file.name
        info.torrent_name = info.file_path.split("/")[-1]
        info.source_button.config(text = info.torrent_name)
        info.opened_torrent = Torrent(info.file_path)
        
        for file in info.file_system.get_children():
            info.file_system.delete(file)

        
        info.fill_the_table()
    #Изменение места расположения будущего файла
    def change_destination(info):
        target_destination = fd.askdirectory(parent=info,initialdir=info.file_dir)
        info.file_dir = target_destination
        info.file_button.config(text=info.file_dir)
    #Установка столбцов для файловой системы
    def set_file_system(info):
        info.file_system['columns'] = ("File","Type","Size")
        #Инициализация столбцов
        info.file_system.column("#0")
        info.file_system.column("File",anchor = "w",width=200,minwidth = 200)
        info.file_system.column("Type",anchor="w",width=70,minwidth = 70)
        info.file_system.column("Size",anchor="w",width=120,minwidth=120)
        #Инициализация строк
        info.file_system.heading("#0")
        info.file_system.heading("File",text="File",anchor="w")
        info.file_system.heading("Type",text="Type",anchor="w")
        info.file_system.heading("Size",text="Size",anchor="w")
    
    def fill_the_table(info):
    
            
        tor = info.opened_torrent
        tor.read_Metafile()

        if tor.kind_file == Torrent.SINGLE_FILE:
            info.n_ame,info.t_ype = dividePrefix(tor.info['name'],".")
            info.t_ype="."+info.t_ype
            info.s_ize = size(tor.info['length'],system=alternative)
            info.file_system.insert(parent="",index = "end",iid=0,values = (info.n_ame,info.t_ype,info.s_ize))
    


#Вспомогательная функция вне класса 
def dividePrefix(path,sym):
    parts  = path.split(sym)
    last_part = parts.pop(-1)
    prefix_part =  sym.join(parts)
    return prefix_part,last_part