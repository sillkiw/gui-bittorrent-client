import tkinter as tk
from tkinter import filedialog as fd

class Mainwin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CrTorrent')
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.set_tool_bar()
        
    
    def set_tool_bar(self):
        #Команда для открытия файловой системы и выбора файла
        def open_file_system(): 
            target_file = fd.askopenfile(filetypes =[('Torrent Files', '*.torrent')]) #Пользователь выбирает торрент файл
            if target_file is not None:
                print(target_file)


        #Главная панель управления (Open|Edit|View)
        main_menu = tk.Menu(self) 

        #Всплывающее окно для File
        file_menu = tk.Menu(tearoff=0)
        file_menu.add_command(label="Open...",command=open_file_system) #Open... открывает обзор файловой системы
        file_menu.add_command(label="Open url...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit")

        #Команды с всплывающими списками
        main_menu.add_cascade(label="File",menu = file_menu)
        main_menu.add_cascade(label="Edit")
        main_menu.add_cascade(label="View")

        #Бинд на окно
        self.config(menu=main_menu)
        
        

if __name__ == "__main__":
    window = Mainwin()
    window.mainloop()