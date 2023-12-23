import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from showinfo import winfoWindow
from install_form import InstallationForm
import sys

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

        #Список установочных форм
        head.installation_form_list = {}

        #Список торрентов
        head.torrent_list = []

        #Установка панели инструментов
        head.set_tool_bar()

        #Установка панели с кнопками
        head.set_button_panel()

        #Установка обзорщика установок
        head.set_viewer()
    
    def ask_torrent_file(head): 
        '''Выбор торрент-файла'''
        #Пользователь выбирает торрент файл
        head.target_torrent = fd.askopenfile(initialdir="C:\\",filetypes =[('Torrent Files', '*.torrent')]) 
        if head.target_torrent:
            head.open_torrent_information_window()

    def set_tool_bar(head):
        '''Установка панели инструментов Open|Edit|View'''

        #Инициализация панели инструментов (Open|Edit|View)
        main_menu = tk.Menu(head) 
       
        #При нажатии на File
        file_menu = tk.Menu(tearoff=0)
        file_menu.add_command(label="Open...",command=head.ask_torrent_file) 
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=sys.exit)
        
        #Инициализация(File|Edit|View) 
        main_menu.add_cascade(label="File",menu = file_menu)
        main_menu.add_cascade(label="Edit")
        main_menu.add_cascade(label="View")
        
        #Бинд на главное окно
        head.config(menu=main_menu)

    def set_button_panel(head):
        head.buttons_frame = tk.Frame(head,background='white')

        head.logo_photo = tk.PhotoImage(file=r"images/logo.png")    
        head.logo_photo = head.logo_photo.subsample(4,5)
        tk.Label(head.buttons_frame,image=head.logo_photo,border=7,background="black").pack(side = tk.LEFT)

        head.delete_button_photo = tk.PhotoImage(file=r"images/delete_button.png")
        head.delete_button_photo = head.delete_button_photo.subsample(2,2)
        
        head.delete_button = tk.Button(head.buttons_frame,highlightcolor='white',text='Delete',foreground="white",activebackground="white",height=55,border=0,background='white',default='active',image=head.delete_button_photo,command=head.delete_torrent)
        head.delete_button.pack(side=tk.LEFT)
        
        
        head.buttons_frame.pack(fill=tk.X)

    def set_viewer(head):
        '''Установка обзорщика установок'''
        head.frame_viewer = tk.Frame(head)

        head.style = ttk.Style()
        
        head.style.configure("mystyle.Treeview",font=('Helvetica',13),foreground='blue')
        head.style.configure("mystyle.Treeview.Heading", background="light ",font=('Helvetica', 11))

        head.viewer = ttk.Treeview(head.frame_viewer,show="headings",style="mystyle.Treeview")
        head.viewer.tag_configure('tor', background='#E8E8E8')
        head.viewer.pack(fill=tk.BOTH,expand=True)
        head.set_columns_and_fill_headings()

        head.frame_viewer.pack(fill=tk.BOTH,expand=True)

    def set_columns_and_fill_headings(head):
        '''Установка столбцов и заполнение заголовков'''
        titles =  ["Name","Size","Progress","Status","Peers","Speed"]

        wid = head.head_width
        sizes = [wid//3+wid//10,wid//14,wid//8,wid//8,wid//14,wid//14]

        head.viewer['columns'] = tuple(titles)

        head.viewer.column("#0")
        head.viewer.heading("#0")

        for index,title in enumerate(titles):
            #Инициализация столбца
            head.viewer.column(title,anchor = "w",width=sizes[index])
            #Инициализация заголовка
            head.viewer.heading(title,text = title,anchor = "w")   

   
    def open_torrent_information_window(head):
        '''Запуск всплывающего окна, если пользователь выбрал файл''' 
        # TODO: Реализовать проверку на дурака(пользователь добавляет один и тот же торрент несколько раз)(проверять части)
        #Инициализация и запуск всплывающего окна
        head.torrent_show = winfoWindow(head) 
        
        head.check_state_of_answer()
                 
    def check_state_of_answer(head):  
        '''Проверка действия пользователя. После нажатия Open в информационном окне начинается установка'''
        
        #Ожидание ответа пользователя
        head.wait_window(head.torrent_show)
        
        if head.torrent_show.state_of_answer == winfoWindow.__States_of_answer__.T_OPENED:
            #Добавление выбранного торрента в список торрентов 
            head.torrent_list.append(head.torrent_show.torrent) 
            #Инициализация и начала установки
            head.initalize_installation()
      
    def initalize_installation(head):
        '''Запуск нового процесса установки'''

        torrent = head.torrent_list[-1]

        #установка id для обновления информации о установке на экране
        id = len(head.torrent_list)

        #Начало установки
        head.installation_form_list[id] = InstallationForm(head,torrent,id)
        head.installation_form_list[id].pack_to_viewer()
        head.installation_form_list[id].begin()



    def delete_torrent(head):
        pass

if __name__ == "__main__":
    window = HeadWindow()
    window.mainloop()