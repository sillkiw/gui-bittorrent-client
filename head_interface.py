import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from showinfo import winfoWindow
from installation_manager import Installation_MNG
import multiprocessing
class HeadWindow(tk.Tk): #главное окно
    def __init__(head):
        super().__init__()    
        head.title('PirTorrent')
        head.head_width = head.winfo_screenwidth()   #ширина главного окна
        head.head_height = head.winfo_screenheight() #высота главного окна
        head.geometry(f"{head.head_width}x{head.head_height}")
        head.iconbitmap("images/icon.ico")
        #Установка просмотрщика установки
        head.viewer = ttk.Treeview(head,show="headings")
        head.fill_viewer_collums()
        head.viewer.pack(fill=tk.BOTH,expand=1,pady=45)
        #Установка панели инструментов
        head.set_tool_bar() 
        
    #Функция создания панели инструментов(Open|Edit|View)
    def set_tool_bar(head):
        #Функция открытия файловой системы и выбора файла
        def open_file_system(): 
            #Пользователь выбирает торрент файл
            head.target_file = fd.askopenfile(filetypes =[('Torrent Files', '*.torrent')]) 
            head.show_info_ab_file()

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
    def show_info_ab_file(head):
        #Jткрытия окна обзорщика файловой системы торрент файла
        #(!)(!)Реализовать проверку на дурака(пользователь добавляет один и тот же торрент несколько раз)(проверять части)
        if  head.target_file != None:
            head.torrent_show = winfoWindow(head) 
            head.check_user_action()

    #Проверка ответа пользователя     
    def check_user_action(head):
        #Ожидание ответа пользователя
        head.wait_window(head.torrent_show)
        if head.torrent_show.state_of_answer == winfoWindow._States_of_answer.T_OPENED:
                head.torrent = head.torrent_show.torrent
                head.tracker.connect_with_tracker()
                #Инициализация установочного менеджера
                head.installation_mng = Installation_MNG(head.torrent)
                #Запуск нового потока
                head.installation_mng.start()
                head.viewer.insert(parent="",index = "end",values = (head.torrent.name,head.torrent_show.s_ize,"0%","Downloading...",f"({head.installation_mng.tracker.amount_of_peers})","None","None"))
    
    #Обзорщик установок
    def fill_viewer_collums(head):
        head.viewer['columns'] = ("Name","Size","Progress","Status","Peers","Speed","Ratio")
        #Инициализация столбцов
        head.viewer.column("#0")
        head.viewer.column("Name",anchor = "w",width=200,minwidth = 200)
        head.viewer.column("Size",anchor="w",width=70,minwidth = 70)
        head.viewer.column("Progress",anchor="w",width=70,minwidth = 70)
        head.viewer.column("Status",anchor="w",width=70,minwidth = 70)
        head.viewer.column("Peers",anchor="w",width=70,minwidth = 70)
        head.viewer.column("Speed",anchor="w",width=70,minwidth = 70)
        head.viewer.column("Ratio",anchor="w",width=70,minwidth = 70)
        #Инициализация строк
        head.viewer.heading("#0")
        head.viewer.heading("Name",text="Name",anchor="w")
        head.viewer.heading("Size",text="Size",anchor="w")
        head.viewer.heading("Progress",text="Progress",anchor="w")
        head.viewer.heading("Status",text="Status",anchor="w")
        head.viewer.heading("Peers",text="Peers",anchor="w")
        head.viewer.heading("Speed",text="Speed",anchor="w")
        head.viewer.heading("Ratio",text="Ratio",anchor="w") 

if __name__ == "__main__":
    window = HeadWindow()
    window.mainloop()