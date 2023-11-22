import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from showinfo import TorrFile_InfoWindow
class HeadWindow(tk.Tk): #главное окно
    def __init__(head):
        super().__init__()
        head.title('PirTorrent')
        
        head.head_width = head.winfo_screenwidth()   #ширина главного окна
        head.head_height = head.winfo_screenheight() #высота главного окна
        head.geometry(f"{head.head_width}x{head.head_height}")
        
        head.iconbitmap("images/icon.ico")
        

        head.set_tool_bar() #Установка панели инструментов

    #Функция создания панели инструментов(Open|Edit|View)
    def set_tool_bar(head):
       
        #Функция открытия файловой системы и выбора файла
        def open_file_system(): 
            #Пользователь выбирает торрент файл
            target_file = fd.askopenfile(filetypes =[('Torrent Files', '*.torrent')]) 
            if target_file is not None:
                head.show_info_ab_file(target_file.name)


        #Инициализация панели инструментов (Open|Edit|View)
        main_menu = tk.Menu(head) 

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

        #Бинд на главное окно
        head.config(menu=main_menu)
   
    #Функция для вызова окна обзорщика файла
    #@param file_name - путь до файла выбранного пользователем
    def show_info_ab_file(head,file_path):
        #Jткрытия окна обзорщика файловой системы торрент файла
        show = TorrFile_InfoWindow(file_path,head.head_width,head.head_height) 
      
        show.mainloop()

        

if __name__ == "__main__":
    window = HeadWindow()
    window.mainloop()