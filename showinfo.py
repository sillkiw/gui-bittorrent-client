import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import font
class TorrFile_InfoWindow(tk.Toplevel):
    #Окно обзорщика торрент файла
    def __init__(info,file_path,head_width,head_height):
         super().__init__()
         
         info.title("Torrent File System ")

         info.info_width = head_width // 2 #Ширина окна
         info.info_height = head_height // 2 #Высота окна

        #Центрирование по центру главного окна(head)
         info.geometry(f"{info.info_width}x{info.info_height}+{(head_width-info.info_width)//2}+{(head_height-info.info_height)//2}")
       
        #Путь до файла выбранного пользователя 
         info.file_path = file_path
         info.file_name = file_path.split("/")[-1]
        
        #Стиль для кнопки и шрифта
         info.info_font = font.Font(family= "Segoe UI", size=10) 
         info.style_button = ttk.Style()
         info.style_button.configure('TButton', anchor=tk.W,font = info.info_font)
        
        #Графа для изменения торрент-файла
         tk.Label(info,text="Torrent sourse:",font=info.info_font).pack()
        #Кнопка для изменения торрент-файла в окне обзорщика торрента
         info.source_photo = tk.PhotoImage(file=r"images/icon.png")
         info.source_photo = info.source_photo.subsample(2,2)
         info.source_button = ttk.Button(info,text = info.file_name,width = info.info_width//20,image=info.source_photo,compound="left",style="TButton",command=info.change_torrent)
         info.source_button.pack()
        
        #Графа для выбора файла, в которой будет помещен торрент
         tk.Label(info,text="Destination:",font=info.info_font).pack()
        #Кнопка
         info.file_photo = tk.PhotoImage(file=r"images/")


    def change_torrent(info):
        target_file = fd.askopenfile(parent = info,initialdir=info.file_path,filetypes =[('Torrent Files', '*.torrent')]) 
        info.file_path = target_file.name
        info.file_name = info.file_path.split("/")[-1]
        info.source_button.config(text = info.file_name)