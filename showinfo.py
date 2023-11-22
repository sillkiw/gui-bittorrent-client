import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
class TorrFile_InfoWindow(tk.Toplevel):
    #Окно обзорщика торрент файла
    def __init__(info,file_path,head_width,head_height):
         super().__init__()
         
         info.title("Torrent File System ")

         info.info_width = head_width // 4 #Ширина окна
         info.info_height = head_height // 4 #Высота окна

         #Центрирование по центру главного окна(head)
         info.geometry(f"{info.info_width}x{info.info_height}+{(head_width-info.info_width)//2}+{(head_height-info.info_height)//2}")
       
         #Путь до файла выбранного пользователя
         info.file_path = file_path

         #Графа для измения торрент-файла
         tk.Label(info,text="Sourse:").pack()
        
         info.file_name = file_path.split("/")[-1] #Имя файла

         #Кнопка для изменения торрент-файла в окне обзорщика торрента
         info.style_button = ttk.Style()
         info.configure('TButton', anchor=tk.W)
         
         
    def set_button(info):
        


    def change_torrent(self,source_path):
        target_file = fd.askopenfile(parent = self,initialdir=source_path,filetypes =[('Torrent Files', '*.torrent')]) 
        self.file_path = target_file.name
        self.file_name = self.file_path.split("/")[-1]
        self.source_button.config(text = self.file_name)