import re
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

# Основное окно
class GUIMain:
      
    def __init__(self):     
        self.main_window = tkinter.Tk()
        self.main_window.title('Для служебного пользования')
        self.main_window.geometry('+100+100')
        self.main_window.resizable(False, False)

        self.name_box()
        self.operation_box()
        self.jobs_box()
        self.choose_save_method()
        self.choose_button()
        self.button_box()
        self.output_options()

        self.select_index = None

    # Список сотрудников
    # Функция заполнения пишется в мейне отдельно
    def name_box(self):
        self.name_frame = tkinter.Frame(self.main_window)
        
        self.name_label = tkinter.Label(self.name_frame,
                                   text='Поверители:')
        self.name_box = tkinter.Listbox(self.name_frame,
                                        selectmode='multiple',
                                        width=20)
        self.name_scrollbar = tkinter.Scrollbar(self.name_frame,
                                           orient='vertical',
                                           command=self.name_box.yview)
        self.name_box.config(yscrollcommand=self.name_scrollbar.set)
        
        self.name_frame.grid(row=0,
                             column=0,
                             padx=10,
                             pady=10)
        self.name_label.pack(side='top',
                             anchor='w')
        self.name_box.pack(side='left')
        self.name_scrollbar.pack(side='right',
                            fill='y',
                            expand=True)
        
        self.name_box.bind('<<ListboxSelect>>',
                           self.select_worker)
##        self.name_box.bind('<Button-1>',
##                           self.select_worker)

    # Редактирование, добавление и удаление сотрудников
    # функция обратного вызова задаётся ..._button.config(command=...
    def operation_box(self):       
        self.operation_frame = tkinter.Frame(self.main_window)
        
        self.create_button = tkinter.Button(self.operation_frame,
                                            text=' + ',
                                            width=4)
        self.update_button = tkinter.Button(self.operation_frame,
                                            text='...',
                                            width=4)        
        self.delete_button = tkinter.Button(self.operation_frame,
                                            text=' - ',
                                            width=4)
        
        self.create_button.pack(side='left')
        self.update_button.pack(side='left')
        self.delete_button.pack(side='left')
        self.operation_frame.grid(row=1,
                                  column=0,
                                  sticky='n',
                                  padx=10,
                                  pady=10)

    # Список выполненных работ,
    # Функция заполнения пишется в мейне отдельно
    def jobs_box(self):       
        self.jobs_frame = tkinter.Frame(self.main_window)
        
        self.jobs_label = tkinter.Label(self.jobs_frame,
                                        text='Список поверок:')
        self.jobs_box = tkinter.Listbox(self.jobs_frame,
                                        width=75)
        self.jobs_scrollbar = tkinter.Scrollbar(self.jobs_frame,
                                                orient='vertical',
                                                command=self.jobs_box.yview)
        self.jobs_box.config(yscrollcommand=self.jobs_scrollbar.set)
        
        self.jobs_frame.grid(row=0,
                             column=1,
                             sticky='ne',
                             padx=10,
                             pady=10)
        self.jobs_label.pack(side='top',
                             anchor='w')
        self.jobs_box.pack(side='left')
        self.jobs_scrollbar.pack(side='right',
                            fill='y',
                            expand=True)

    # Выбор черновик/отправлено
    def choose_save_method(self):
        self.radio_frame = tkinter.Frame(self.main_window)
        
        self.switch_status = tkinter.IntVar()
        self.switch_status.set(1)
        self.radio_draft = tkinter.Radiobutton(self.radio_frame,
                                               text='Черновик',
                                               variable=self.switch_status,
                                               value=1)
        self.radio_sent = tkinter.Radiobutton(self.radio_frame,
                                              text='Отправлено',
                                              variable=self.switch_status,
                                              value=2)
        
        self.radio_draft.pack(anchor='w')
        self.radio_sent.pack(anchor='w')

        self.radio_frame.grid(row=3,
                              column=1,
                              sticky='sw',
                              padx=10,
                              pady=10)

    # Кнопка диалога для выбора файлов,
    # функция обратного вызова задаётся choose_button.config(command=
    def choose_button(self):
        self.choose_button = tkinter.Button(self.main_window,
                                            text='Взять из архива',
                                            width=14)
        
        self.choose_button.grid(row=1,
                                column=1,
                                sticky='ne',
                                padx=10,
                                pady=10)

    # Основные кнопки, функция обратного вызова задаётся perform.config(command=...
    def button_box(self):
        self.button_frame = tkinter.Frame(self.main_window)
        
        self.perform = tkinter.Button(self.button_frame,
                                      text='В XML',
                                      width=8)
        self.quit = tkinter.Button(self.button_frame,
                                   text='Выход',
                                   width=8,
                                   command=self.main_window.destroy)
        
        self.perform.pack(side='right')
        self.quit.pack(side='right')
        self.button_frame.grid(row=3,
                               column=1,
                               sticky='se',
                               padx=10,
                               pady=10)

    # Выбор    
    def select_worker(self, event):
        try:
            self.select_index = self.name_box.curselection()
##            self.select_index = self.select_index[0]
            print('Выбрано по индексу: ' + str(list(self.select_index)))
        except IndexError:
            self.select_index = None
            print('Шлёп, индекс улетел')
    # Опции
    def output_options(self):
        self.opt_frame = tkinter.Frame(self.main_window)
        self.opt_label = tkinter.Label(self.opt_frame,
                                       text='Опции:')
        self.full_enabled = tkinter.IntVar(value=1)
        self.full_certificate = tkinter.Checkbutton(self.opt_frame,
                                                     text='Указывать шифр в номере свидетельства',
                                                     variable=self.full_enabled)
        self.opt_label.pack(anchor='w')
        self.full_certificate.pack(anchor='w')
        self.opt_frame.grid(row=2,
                            column=0,
                            columnspan=2,
                            sticky='nw',
                            padx=10,
                            pady=10)
    
# Окно создания работяги
class GUIEmployee():

    def __init__(self):
        
        self.employ_window = tkinter.Toplevel()
        self.employ_window.title('Работяги')
        self.employ_window.geometry('300x200+150+150')
        self.employ_window.resizable(False, False)
        
        self.entry_frame = tkinter.Frame(self.employ_window)
        
        self.label_first = tkinter.Label(self.entry_frame, text='Имя')
        self.label_last = tkinter.Label(self.entry_frame, text='Фамилия')
        self.label_middle = tkinter.Label(self.entry_frame, text='Отчество')
        self.label_SNILS = tkinter.Label(self.entry_frame, text='СНИЛС')       

        self.entry_first = tkinter.Entry(self.entry_frame, width=100)
        self.entry_last = tkinter.Entry(self.entry_frame, width=100)
        self.entry_middle = tkinter.Entry(self.entry_frame, width=100)

        self.pattern = re.compile('^\d{0,11}$')
        vcmd = (self.employ_window.register(self.valid_SNILS), '%i', '%P')
        self.entry_SNILS = tkinter.Entry(self.entry_frame, width=100,
                                         validate='key',
                                         validatecommand=vcmd,
                                         invalidcommand=lambda: print('Это не СНИЛС'))

        self.label_last.grid(row=0, column=0, sticky='se')
        self.label_first.grid(row=1, column=0, sticky='se')
        self.label_middle.grid(row=2, column=0, sticky='se')
        self.label_SNILS.grid(row=3, column=0, sticky='se')
                
        self.entry_last.grid(row=0, column=1)
        self.entry_first.grid(row=1, column=1)
        self.entry_middle.grid(row=2, column=1)      
        self.entry_SNILS.grid(row=3, column=1)

        self.entry_frame.pack(anchor='nw',
                              padx=10,
                              pady=10)

        self.button_box()
        self.employ_window.grab_set()

    # Валидация СНИЛСа
    def valid_SNILS(self, index, SNILS):
        print('Проверка символа: ' + index)
        return self.pattern.match(SNILS) is not None
        
    # Пак кнопок управления
    # Функция обратного вызова устанавливается через perform.config
    def button_box(self):
        self.button_frame = tkinter.Frame(self.employ_window)
        
        self.perform = tkinter.Button(self.button_frame,
                                      text='Добавить',
                                      width=8)                   
        self.quit = tkinter.Button(self.button_frame,
                                   text='Выход',
                                   width=8,
                                   command=self.employ_window.destroy)
        
        self.quit.pack(side='right')
        self.perform.pack(side='right')
        self.button_frame.pack(side='bottom',
                               anchor='se',
                               padx=10,
                               pady=10)

# Окно редактирования работяг
# Это наследник класса создания работяги
# Отличие от создания только в кнопке
# Функция обратного вызова прописывается через .config кнопки класса родителя
class GUIEmployeeUpdate(GUIEmployee):

    def __init__(self):
        GUIEmployee.__init__(self)

        self.perform.config(text='Изменить')

# Прогрессбар отображает процесс загрузки,
# метод апдейт необходим, чтобы обновлять окно и приходящие дааные,
# метод лифт поднимает окно поверх других
# Все настройки, такие как текущее положение бара и
# максимальное положение бара прописываются в load_bar.config экземпляра
class GUIProgressLoad():

    def __init__(self):
        self.progress_window = tkinter.Toplevel()
        self.progress_window.title('Загружаем')
        self.progress_window.geometry('+200+200')

        self.load_bar = ttk.Progressbar(self.progress_window,
                                        length=200)
        self.load_bar.pack(fill='x',
                           padx=10,
                           pady=10)
        
        self.progress_window.lift()
        self.progress_window.update()
        
if __name__ == '__main__':
    tkinter.mainloop()
        
