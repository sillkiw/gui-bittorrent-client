import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from showinfo import winfoWindow
from installation_manager import Installation_MNG
from multiprocessing import Pipe
import threading
class HeadWindow(tk.Tk): #главное окно
    def __init__(head):
        super().__init__()    
        head.title('PirTorrent')
        head.sc_width = head.winfo_screenwidth()
        head.sc_height = head.winfo_screenheight()
        head.head_width = head.sc_width//2 + head.sc_width//4 #ширина главного окна
        head.head_height = head.sc_height//2 + head.sc_height//4 #высота главного окна
        head.geometry(f"{head.head_width}x{head.head_height}+{(head.sc_width - head.head_width)//2}+{(head.sc_height - head.head_height -100)//2}")
        head.iconbitmap("images/icon.ico")
        #Инициализация списка труб для передачи информации между процессами
        head.amount_of_installation = 0
        head.pipes_list = []
        head.torrent_list = []
        #Обзорщик установок
        head.number_of_torrent = 0
        head.frame_viewer = tk.Frame(head)
        head.viewer = ttk.Treeview(head.frame_viewer,show="headings")
        head.viewer.pack(fill=tk.BOTH,expand=True)
        head.fill_viewer_collums()
        head.frame_viewer.pack(fill=tk.BOTH,expand=True)
        #Установка панели инструментов
        head.set_tool_bar() 
        
    #Функция создания панели инструментов(Open|Edit|View)
    def set_tool_bar(head):
        #Функция открытия файловой системы и выбора файла
        def open_file_system(): 
            #Пользователь выбирает торрент файл
            head.target_torrent = fd.askopenfile(filetypes =[('Torrent Files', '*.torrent')]) 
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
        # TODO: Реализовать проверку на дурака(пользователь добавляет один и тот же торрент несколько раз)(проверять части)
        if  head.target_torrent != None:
            head.torrent_show = winfoWindow(head) 
            head.check_user_action()
            

    #Проверка ответа пользователя     
    def check_user_action(head):  
        #Ожидание ответа пользователя
        head.wait_window(head.torrent_show)
        if head.torrent_show.state_of_answer == winfoWindow._States_of_answer.T_OPENED:
                #Добавление выбранного торрента в список торрентов 
          
                head.torrent_list.append(head.torrent_show.torrent) 
                
                #Инициализация и начала установки
                head.initalize_installation()
    
    #Функция для потоков для обновления информации об установочном процессе 
    def updater(head,id,from_install,name,size):
        while True:
            progress,status,peers= from_install.recv()
            head.viewer.item(id,text = "",values=(name,size,progress,status,peers))
    
    #Инициализация и начала установки
    def initalize_installation(head):
        torrent = head.torrent_list[-1]
        #Размещение строки в обзорщик установки
        head.viewer.insert(parent="",index = "end",iid = head.number_of_torrent,
                           values = (torrent.name,torrent.size,"0%","Downloading...","0(0)"))
        #Нужно сохранять трубы в массив,а иначе не работает
        head.pipes_list.append(Pipe())
        to_head,from_install = head.pipes_list[-1]
        #Инициализация установочного менеджера
        Installation_MNG(torrent,to_head).start()
        #Запуск нового потока для обновления информации на экране
        threading.Thread(target=head.updater,args=(head.number_of_torrent,from_install,torrent.name,torrent.size)).start()
        #Увеличение счетчика 
        head.number_of_torrent+=1

    #Обзорщик установок
    def fill_viewer_collums(head):
        columns =  ["Name","Size","Progress","Status","Peers"]
        head.viewer['columns'] = tuple(columns)
        head.viewer.column("#0")
        head.viewer.heading("#0")
        for inf in columns:
            #Инициализация столбцов
            head.viewer.column(inf,anchor = "w")
            #Инициализация строк
            head.viewer.heading(inf,text = inf,anchor = "w")
 

if __name__ == "__main__":
    window = HeadWindow()
    window.mainloop()