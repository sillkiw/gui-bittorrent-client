import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox
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

        head.set_style()

        #Установка панели инструментов
        head.set_tool_bar()

        #Установка панели с кнопками
        head.set_button_panel()

        #Установка обзорщика установок
        head.set_viewer()
    
    def ask_torrent_file(head,chest = False): 
        '''Выбор торрент-файла'''
        if chest:
            head.chest_button.configure(image=head.open_chest_button_photo)
        
        head.chest = chest
        
        #Пользователь выбирает торрент файл
        head.target_torrent = fd.askopenfile(initialdir="C:\\",filetypes =[('Torrent Files', '*.torrent')]) 
        
        if head.target_torrent:
            head.open_torrent_information_window()
        elif chest:
            head.chest_button.configure(image=head.chest_button_photo)
            
    
    def set_tool_bar(head):
        '''Установка панели инструментов Open|Edit|View'''

        #Инициализация панели инструментов (Open|Edit|View)
        main_menu = tk.Menu(head) 
       
        #При нажатии на File
        file_menu = tk.Menu(tearoff=0)
        file_menu.add_command(label="Открыть...",command=head.ask_torrent_file) 
        file_menu.add_separator()
        file_menu.add_command(label="Выйти",command=sys.exit)
        
        edit_menu = tk.Menu(tearoff=0)
        edit_menu.add_command(label="Начать все загрузки",command=head.start_all)
        edit_menu.add_command(label="Остановить все загрузки",command=head.stop_all)
        edit_menu.add_separator()
        edit_menu.add_command(label="Удалить все загрузки",command=head.delete_all)

        #Инициализация(File|Edit|View) 
        main_menu.add_cascade(label="Файл",menu = file_menu)
        main_menu.add_cascade(label="Правка",menu = edit_menu)
     
        #Бинд на главное окно
        head.config(menu=main_menu)

    def start_all(head):
        for id in head.installation_form_list:
            head.installation_form_list[id].status.value = InstallationForm.RUN
   
    def delete_all(head):
        for install in head.viewer.get_children():
            head.viewer.delete(install)
        for id in head.installation_form_list:
            head.installation_form_list[id].status.value = InstallationForm.DELETE
    
    def stop_all(head):
        for id in head.installation_form_list:
            head.installation_form_list[id].status.value = InstallationForm.STOP


    def set_button_panel(head):
        head.buttons_frame = tk.Frame(head,background='white')

        head.logo_photo = tk.PhotoImage(file=r"images/logo.png")    
        head.logo_photo = head.logo_photo.subsample(4,5)
        tk.Label(head.buttons_frame,image=head.logo_photo,border=7,background="black").pack(side = tk.LEFT)

    
        head.start_button_photo = tk.PhotoImage(file=r"images/play_button.png")
        head.start_button_photo = head.start_button_photo.subsample(7,8)
        
        head.start_button = tk.Button(head.buttons_frame,highlightcolor='white',text='Delete',foreground="white",width = 80,activebackground="white",height=60,border=0,background='white',default='active',image=head.start_button_photo,command=head.start_torrent)
        head.start_button.pack(side=tk.LEFT)

        head.stop_button_photo = tk.PhotoImage(file=r"images/stop_button.png")
        head.stop_button_photo = head.stop_button_photo.subsample(4,4)
        
        head.stop_button = tk.Button(head.buttons_frame,highlightcolor='white',text='Delete',foreground="white",width = 80,activebackground="white",height=60,border=0,background='white',default='active',image=head.stop_button_photo,command=head.stop_torrent)
        head.stop_button.pack(side = tk.LEFT)

        head.delete_button_photo = tk.PhotoImage(file=r"images/delete_button.png")
        head.delete_button_photo = head.delete_button_photo.subsample(9,9)
        
        head.delete_button = tk.Button(head.buttons_frame,highlightcolor='white',text='Delete',foreground="white",width = 80,activebackground="white",height=60,border=0,background='white',default='active',image=head.delete_button_photo,command=head.delete_torrent)
        head.delete_button.pack(side=tk.LEFT)
        

        
    
        head.chest_button_photo = tk.PhotoImage(file=r"images/chest.png")
        head.open_chest_button_photo = tk.PhotoImage(file=r"images/chest_open.png")
        head.chest_button_photo = head.chest_button_photo.subsample(8,8)
        head.open_chest_button_photo = head.open_chest_button_photo.subsample(10,10)
        head.chest = False

        head.chest_button = tk.Button(head.buttons_frame,highlightcolor='white',text='Delete',foreground="white",activebackground="white",height=55,width=100,border=0,background='white',default='active',image=head.chest_button_photo,command=lambda : head.ask_torrent_file(chest = True))
        head.chest_button.pack(side=tk.LEFT,padx=40)

   

        head.buttons_frame.pack(fill=tk.X)
    
    def start_torrent(head):
        try:
            selected = int(head.viewer.focus())
            head.installation_form_list[selected].status.value = InstallationForm.RUN
        except Exception:
            pass

    def stop_torrent(head):
        try:
            selected = int(head.viewer.focus())
            head.installation_form_list[selected].status.value = InstallationForm.STOP
        except Exception:
            pass


    def set_viewer(head):
        '''Установка обзорщика установок'''
        head.frame_viewer = tk.Frame(head)

        head.viewer = ttk.Treeview(head.frame_viewer,show="headings",style="mystyle.Treeview")
        head.viewer.tag_configure('tor', background='#E8E8E8')
        head.viewer.pack(fill=tk.BOTH,expand=True)
        head.set_columns_and_fill_headings()

        head.frame_viewer.pack(fill=tk.BOTH,expand=True)

    def set_columns_and_fill_headings(head):
        '''Установка столбцов и заполнение заголовков'''
        titles =  ["Имя","Размер","Прогресс","Статус","Пиры","Скорость"]

        wid = head.head_width
        sizes = [wid//3+wid//10,wid//14,wid//8,wid//8,wid//14,wid//14]

        head.viewer['columns'] = tuple(titles)

        head.viewer.column("#0")
        head.viewer.heading("#0")

        for index,title in enumerate(titles):
            #Инициализация столбц
            head.viewer.column(title,anchor = "w",width=sizes[index])
            #Инициализация заголовка
            head.viewer.heading(title,text = title,anchor = "w")   

    def set_style(head):
        head.style = ttk.Style()
        
        head.style.configure("mystyle.Treeview",font=('Helvetica',13),foreground='blue')
        head.style.configure("mystyle.Treeview.Heading", background="light ",font=('Helvetica', 11))


   
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
        
        if head.chest:
           head.chest_button.configure(image=head.chest_button_photo)

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
        head.installation_form_list[id] = InstallationForm(head,torrent,id,head.torrent_show.size)
        head.installation_form_list[id].pack_to_viewer()
        head.installation_form_list[id].begin()


    def delete_torrent(head):
        try:
            selected = int(head.viewer.focus())
            if selected != '':            
                if messagebox.askyesno("Удаление торрент-файла","Вы уверены, что хотите удалить торрент-файл?"):
                    head.viewer.delete(selected)
                    head.installation_form_list[selected].status.value = InstallationForm.DELETE
        except Exception as e :
            pass

if __name__ == "__main__":
    window = HeadWindow() 
    window.mainloop()