import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
class ShowInfo(tk.Toplevel):
    def __init__(self,file_path,width_s,heigh_s):
         super().__init__()
         
         self.title("File System inside torrent")
         self.geometry(f"{width_s // 3}x{heigh_s // 3}")
         self.file_path = file_path

         self.source_text = tk.Label(self,text="Sourse:")
         self.source_text.pack()

         file_name = file_path.split("/")[-1]
         self.source_button = ttk.Button(self,text=file_name,command= lambda  : self.change_torrent(file_path))
         self.source_button.pack()
         
       

    def change_torrent(self,source_path):
        target_file = fd.askopenfile(parent = self,initialdir=source_path,filetypes =[('Torrent Files', '*.torrent')]) 
        self.file_path = target_file.name
        self.file_name = self.file_path.split("/")[-1]
        self.source_button.config(text = self.file_name)