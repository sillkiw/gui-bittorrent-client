import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from showinfo import ShowInfo
class Mainwin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CrTorrent')
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        
        self.set_tool_bar()

    #Создания панели инструментов(Open|Edit|View)
    def set_tool_bar(self):
       
        #Функция открытия файловой системы и выбора файла
        def open_file_system(): 
            #Пользователь выбирает торрент файл
            target_file = fd.askopenfile(filetypes =[('Torrent Files', '*.torrent')]) 
            if target_file is not None:
                self.show_info_ab_file(target_file.name)


        #Инициализация панели инструментов (Open|Edit|View)
        main_menu = tk.Menu(self) 

        #Всплывающее окно для File
        file_menu = tk.Menu(tearoff=0)
        file_menu.add_command(label="Open...",command=open_file_system) #Open... открывает обзор файловой системы
        file_menu.add_command(label="Open url...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit")

        #Инициализация(File|Edit|View) 
        main_menu.add_cascade(label="File",menu = file_menu)
        main_menu.add_cascade(label="Edit")
        main_menu.add_cascade(label="View")

        #Бинд на экран
        self.config(menu=main_menu)
    def show_info_ab_file(self,file_name):
        show = ShowInfo(file_name,self.winfo_screenwidth(),self.winfo_screenheight())
        show.mainloop()

        

if __name__ == "__main__":
    window = Mainwin()
    window.mainloop()