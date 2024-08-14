import os
import pathlib
import pickle
import employees
import gui2
from pypdf import PdfReader
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from zipfile import BadZipFile

##    Главное окно приложения
def main():
    PATH_CWD = pathlib.Path.cwd()
    PATH_CFG = pathlib.Path(PATH_CWD, 'data', 'config.cfg')
    OPTIONS = {}
    
    try:
        file = open(PATH_CFG, 'rb')
    except FileNotFoundError:
        try:
            os.mkdir('data')
        except FileExistsError:
            pass
        finally:
            with open(PATH_CFG, 'wb') as new_file:
                OPTIONS = {'full_num_cert': 0,
                           'draft_or_sent': 1,
                           'path_to_file': PATH_CFG}
                pickle.dump(OPTIONS, new_file)
    else:
        with file:
            OPTIONS = pickle.load(file)

    print(OPTIONS)
    
    open_window_main(OPTIONS)

##    Функция создания работяги
##    Работяга - экземпляр класса со своими методами из employees
##    Функция сохраняет файл с ФИО и СНИЛС в двоичном формате
##    но не особо безопастно
##    методы для дотупа к атрибутам класса прописаны в employees
def create(first, last, middle, SNILS):
    usr_employ = employees.Employee()
    
    usr_employ.set_first(first)
    usr_employ.set_last(last)
    usr_employ.set_middle(middle)
    usr_employ.set_SNILS(SNILS)

    usr = read()
    exist = False

    path = pathlib.Path.cwd()
    path = pathlib.Path(path, 'data', 'employees.dat')
    print(path)
    
    if usr:
        for item in usr:
            if item.get_SNILS() == SNILS:
                print('Запись существует')
                exist = True

    if not exist:
        try:
            open(path, 'ab')
        except IOError:
            print('Создаём директорию')
##            os.mkdir('data')
        finally:
            with open(path, 'ab') as file:
                pickle.dump(usr_employ, file)
                print('Новый работяга добавлен')

##    Читает файл с сотрудниками и возвращает список с объектами             
def read():
    employee = []
    path = pathlib.Path.cwd()
    path = pathlib.Path(path, 'data', 'employees.dat')
    
    try:
        open(path, 'rb')
    except IOError as err:
        print(err)
    else:
        with open(path, 'rb') as file:
            while True:
                try:
                    employee.append(pickle.load(file))
                except EOFError:
                    break
            return employee

##    Функция обновления работяги
def update(old_obj, new_obj):
    usr_obj = read()
    
    path = pathlib.Path.cwd()
    path = pathlib.Path(path, 'data', 'employees.dat')
    
    if usr_obj is not None:
        for obj in usr_obj:
            if obj.get_SNILS() == old_obj.get_SNILS():
                index = usr_obj.index(obj)
                usr_obj[index] = new_obj
                with open(path, 'wb') as file:
                    for obj in usr_obj:
                        pickle.dump(obj, file)
        print('Информация о сотруднике обновлена')

##    Функция удаления работяги с записью в файл
def delete2(obj_to_delete):
    path = pathlib.Path.cwd()
    path = pathlib.Path(path, 'data', 'employees.dat')

    if obj_to_delete is not None:
        usr = read()        
        if usr is not None:
            for obj in usr:
                if obj.get_SNILS() == obj_to_delete.get_SNILS():
                    usr.remove(obj)
        with open(path, 'wb') as file:
            for obj in usr:
                pickle.dump(obj, file)
        print('Запись удалена')

##    Эта собирает информацию из ПДФ файлов в текст и записывает в файл jobs.dat
def collect(files):  
    # Ключи поиска: начало и конец
    RESULT_GOOD = 'СВИДЕТЕЛЬСТВО О ПОВЕРКЕ №'
    RESULT_GOOD_STOP = 'Действительно до'
    RESULT_BAD = 'ИЗВЕЩЕНИЕ О НЕПРИГОДНОСТИ К ПРИМЕНЕНИЮ №'
    RESULT_BAD_STOP = 'Средство измерений'
    VERIFICATOR = 'Поверитель'
    VERIFICATOR_STOP = 'фамилия'
    VER_DATE = 'Дата поверки'
    VER_DATE_STOP = 'Выписка'
    VER_EXP_DATE = 'Действительно до'
    VER_EXP_DATE_STOP = 'Средство измерений'
    TYPE_MES_INST = 'Средство измерений'
    TYPE_MES_INST_STOP = 'Рег.'
    TYPE_ARTEFACT = 'номер в'

    # Экземпляр класса данных для формирования xml
    my_data = employees.SendingData()

    # Парсинг pdf файлов
    reader = PdfReader(files)
    result = ''
    for page in reader.pages:
        result += page.extract_text()
    
    # Наполняем наш экземпляр данными
    # Годен - 1 или не годен - 2
    if result.find(RESULT_BAD) != -1:
        rvt = '2'
    if result.find(RESULT_GOOD) != -1:
        rvt = '1'

    # Имена сотрудников
    index = result.find(VERIFICATOR)
    stop = result.find(VERIFICATOR_STOP)
    name = result[index + len(VERIFICATOR) : stop].strip('_').split()

    # Номер свидетельства о поверке
    if result.find(RESULT_BAD) != -1: 
        index = result.find(RESULT_BAD)
        stop = result.find(RESULT_BAD_STOP)
        number = result[index + len(RESULT_BAD) : stop].strip().split('/')
        number = number[-1]
        full_number = result[index + len(RESULT_BAD) : stop].strip()
    if result.find(RESULT_GOOD) != -1:
        index = result.find(RESULT_GOOD)
        stop = result.find(RESULT_GOOD_STOP)        
        number = result[index + len(RESULT_GOOD) : stop].strip().split('/')
        number = number[-1]
        full_number = result[index + len(RESULT_GOOD) : stop].strip()

    # Дата поверки
    index = result.find(VER_DATE)
    stop = result.find(VER_DATE_STOP)
    date = result[index + len(VER_DATE) : stop].lstrip().strip('\n').split('.')
    if len(date[0]) > 2:
        date[0] = date[0][-2:]
    date.reverse()
    date = '-'.join(date)
    
    if result.find(RESULT_GOOD) != -1:
        index = result.find(VER_EXP_DATE)
        stop = result.find(VER_EXP_DATE_STOP)
        date_ends = result[index + len(VER_EXP_DATE) : stop].lstrip().strip('\n').split('.')
        date_ends.reverse()
        date_ends = '-'.join(date_ends)
    else:
        date_ends = date
        
    index = result.find(TYPE_MES_INST)
    stop = result.find(TYPE_MES_INST_STOP)
    type_me = result[index + len(TYPE_MES_INST) : stop].strip('_').split(';')
    artefact = type_me[2]
    
    if artefact.find(TYPE_ARTEFACT) != -1:
        index = artefact.find(TYPE_ARTEFACT)
        type_me[2] = ' ' + artefact[index + len(TYPE_ARTEFACT):]
    type_me = type_me[0] + type_me[2]
    print(type_me)
    
    # Формируем массив данных
    my_data.set_ResultVerificationIdType(rvt)
    my_data.set_TypeSaveMethod('2')
    my_data.set_SNILS('Не задано')
    my_data.set_NameType('')
    my_data.set_Last(name[0])
    my_data.set_First(name[1])
    my_data.set_Middle(name[2])
    my_data.set_VerificationMesuringInstrument('')
    my_data.set_NumberVerification(number)
    my_data.set_DateVerification(date)
    my_data.set_DateEndVerification(date_ends)
    my_data.set_TypeMeasuringInstrument(type_me)
    my_data.set_FullNumberVerification(full_number)

    return my_data

##    Эта конвертирует в XML
def convert(data, full_status):

    # Создаём корневой тег и пару подтегов
    message = ET.Element('Message')
    message.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    message.set('xsi:noNamespaceSchemaLocation', 'schema.xsd')
    record = ET.SubElement(message, 'VerificationMeasuringInstrumentData')
    
    # Сохранить как черновик либо "Отправлено"
    TSM = ET.SubElement(message, 'SaveMethod')
    
    # Заполняем текстовые поля тегов
    for item in data:
        VMI = ET.SubElement(record, 'VerificationMeasuringInstrument')

        # Описание поверяемого прибора
        NV = ET.SubElement(VMI, 'NumberVerification')
        DV = ET.SubElement(VMI, 'DateVerification')
        DEV = ET.SubElement(VMI, 'DateEndVerification')
        TMI = ET.SubElement(VMI, 'TypeMeasuringInstrument')

        # Информация о поверителе и результат
        AE = ET.SubElement(VMI, 'ApprovedEmployee')
        N = ET.SubElement(AE, 'Name')
        L = ET.SubElement(N, 'Last')
        F = ET.SubElement(N, 'First')
        M = ET.SubElement(N, 'Middle') 
        SNILS = ET.SubElement(AE, 'SNILS')
        RV = ET.SubElement(VMI, 'ResultVerification')
        
        print(item.get_TypeMeasuringInstrument())

        # Заполняем поля данными из файла
        RV.text = item.get_ResultVerificationIdType()
        TSM.text = item.get_TypeSaveMethod()
        SNILS.text = item.get_SNILS()
        L.text = item.get_Last()
        F.text = item.get_First()
        M.text = item.get_Middle()
        VMI.text = item.get_VerificationMesuringInstrument()
        if full_status:
            NV.text = item.get_FullNumberVerification()
        else:
            NV.text = item.get_NumberVerification()
        DV.text = item.get_DateVerification()
        DEV.text = item.get_DateEndVerification()
        TMI.text = item.get_TypeMeasuringInstrument()

    # Создаём дерево
    tree = ET.ElementTree(message)
    ET.indent(tree)

    # Сохраняем
    tree.write('toload.xml', encoding='UTF-8', xml_declaration=True)
##    print("Сохранено в файл 'toload.xml'")
##    print(ET.dump(message))
    gui2.messagebox.showinfo(title='Успех!',
                             message='Файл XML сформирован')

##    Тут начинается настройка окон,
##    работы функций обратного вызова и тп
def open_window_main(options):
    my_window_main = gui2.GUIMain()
    my_window_main.full_enabled.set(options['full_num_cert'])
    my_window_main.switch_status.set(options['draft_or_sent'])
        
    refresh_name_box_window_main(my_window_main)

    my_window_main.create_button.config(
        command=lambda: open_window_create(my_window_main)
        )
    my_window_main.update_button.config(
        command=lambda: open_window_update(selected(my_window_main), my_window_main)
        )
    my_window_main.delete_button.config(
        command=lambda: delete_worker(selected(my_window_main), my_window_main)
        )
    my_window_main.choose_button.config(
        command=lambda: full_load_refresh(my_window_main)
        )
    my_window_main.perform.config(
        command=lambda: convert_to_xml_all(selected(my_window_main), my_window_main)
        )
    my_window_main.quit.config(
        command=lambda: exit_programm(my_window_main, options)
        )

    my_window_main.name_box.bind('<<ListboxSelect>>',
                                 lambda event: re_select(event, my_window_main))

##    Обработчик события выбора сотрудника, почти декоратор
def re_select(event, window_main):
    window_main.select_worker(event)
    refresh_jobs_box_window_main(window_main)

##    Возвращает выбранных из списка сотрудников в качестве списка объектов
def selected(main_window):
    employees = read()
    selected_obj = []
    try:
        for index_in_box in main_window.select_index:
            selected_obj.append(employees[index_in_box])
        return selected_obj
    except TypeError:
        gui2.messagebox.showerror(title='Ошибко',
                                  message='Надо выбрать кого-нибудь')
        return None

##    Создаёт окно для добавления нового сотрудника
def open_window_create(window_main):
    my_employee = gui2.GUIEmployee()

    my_employee.perform.config(command=lambda: create_worker(my_employee,
                                                             window_main))

def create_worker(window_create, window_main):
    create(window_create.entry_first.get(),
           window_create.entry_last.get(),
           window_create.entry_middle.get(),
           window_create.entry_SNILS.get())
    
    refresh_name_box_window_main(window_main)
    window_create.employ_window.destroy()

##    if window_main.jobs_box.size() != 0:
##        gui2.messagebox.showinfo(title='Инфо',
##                                 message='Пожалуйста перезагрузите архив')
##        window_create.employ_window.lift()

##  Создаёт окно для редактирования существующих сотрудников    
def open_window_update(obj_to_update, window_main):
    if obj_to_update is None:
        print('Никого не выбрано')
    elif len(obj_to_update) == 1:
        obj_to_update = obj_to_update[0]
        my_employee_u = gui2.GUIEmployeeUpdate()

        my_employee_u.entry_first.insert(0, obj_to_update.get_first())
        my_employee_u.entry_last.insert(0, obj_to_update.get_last())
        my_employee_u.entry_middle.insert(0, obj_to_update.get_middle())
        my_employee_u.entry_SNILS.insert(0, obj_to_update.get_SNILS())
        
        my_employee_u.perform.config(command=lambda: update_worker(obj_to_update,
                                                                   my_employee_u,
                                                                   window_main))
    else:
        print('Нужно выбрать кого-то одного')
        gui2.messagebox.showinfo(title='Инфо',
                         message='Нужно выбрать кого-то одного')
        window_main.name_box.select_clear(first=0,
                                          last=window_main.name_box.size()-1)

def update_worker(old_emp, window_update, window_main):
    upd_employee = employees.Employee()
    
    upd_employee.set_first(window_update.entry_first.get())
    upd_employee.set_last(window_update.entry_last.get())
    upd_employee.set_middle(window_update.entry_middle.get())
    upd_employee.set_SNILS(window_update.entry_SNILS.get())

    update(old_emp, upd_employee)
    refresh_name_box_window_main(window_main)
    window_update.employ_window.destroy()

##    if window_main.jobs_box.size() != 0:
##        gui2.messagebox.showinfo(title='Инфо',
##                                 message='Пожалуйста перезагрузите архив')
##        window_update.employ_window.lift()

def delete_worker(obj_to_delete, window_main):
    if obj_to_delete is None:
        print('Никого не выбрано')
    elif len(obj_to_delete) != 1:
        print('Нужно выбрать кого-то одного')
        gui2.messagebox.showinfo(title='Инфо',
                         message='Нужно выбрать кого-то одного')
        window_main.name_box.select_clear(first=0,
                                          last=window_main.name_box.size()-1)
    else:
        obj_to_delete = obj_to_delete[0]
        delete2(obj_to_delete)
        refresh_name_box_window_main(window_main)
##        if window_main.jobs_box.size() != 0:
##            gui2.messagebox.showinfo(title='Инфо',
##                                     message='Пожалуйста перезагрузите архив')

##    Обновляет список сотрудников       
def refresh_name_box_window_main(window_main):
    employees = read()
    window_main.name_box.delete(0, gui2.tkinter.END)
    if employees:
        for obj in employees:
            window_main.name_box.insert(gui2.tkinter.END,
                                        obj.get_first() + ' ' + obj.get_last())

##    Загружает работы, выполненные сотрудниками из архива в файл
def load_jobs():
    path = pathlib.Path.cwd()
    path = pathlib.Path(path, 'data', 'jobs.dat')

    my_file = gui2.filedialog.askopenfilename()
    if my_file:
        try:
            with ZipFile(my_file, 'r') as my_zip:
                my_data_all = []
                load_bar = gui2.GUIProgressLoad()
                load_bar.load_bar.config(maximum=len(my_zip.namelist()))
                for item in my_zip.namelist():
                    print(item)
                    with my_zip.open(item, 'r') as unzipped_file:
                        data = collect(unzipped_file)
                        my_data_all.append(data)
                    load_bar.load_bar.config(value=my_zip.namelist().index(item)+1)
                    load_bar.load_bar.update()
                load_bar.progress_window.destroy()
            with open(path, 'wb') as file:
                pickle.dump(my_data_all, file)
        except BadZipFile:
            print('Это не архив')
            gui2.messagebox.showinfo(title='Инфо',
                                     message='Это не файл архива')

##    Считывает файл с выполненными работами, возвращает список объектов выполненных работ
def read_jobs():
    path = pathlib.Path.cwd()
    path = pathlib.Path(path, 'data', 'jobs.dat')

    try:
        open(path, 'rb')
    except IOError:
        print('Файла jobs.dat нет')
    else:
        with open(path, 'rb') as file:
            jobs = pickle.load(file)
            return jobs

##    Удаляет файл с работами
def del_jobs_file():
    path = pathlib.Path.cwd()
    path = pathlib.Path(path, 'data', 'jobs.dat')

    try:
        os.remove(path)
    except OSError:
        print('Файла не существует')

##    Обновление списка работ в соответствии с выбранным сотрудником
def refresh_jobs_box_window_main(window_main):
    jobs = read_jobs()
    if jobs is None:
        print('Загрузи архив')
    else:
        window_main.jobs_box.delete(0, gui2.tkinter.END)
        if window_main.select_index is None or not window_main.select_index:
            for item in jobs:
                window_main.jobs_box.insert(gui2.tkinter.END,
                                            item.get_NumberVerification() + ' ' +
                                            item.get_TypeMeasuringInstrument())
        else:
            worker_selected = selected(window_main)
            for worker in worker_selected:
                for item in jobs:
                    if (worker.get_first() + worker.get_last() + worker.get_middle() ==
                        item.get_First() + item.get_Last() + item.get_Middle()):                
                        window_main.jobs_box.insert(gui2.tkinter.END,
                                                    item.get_NumberVerification() + ' ' +
                                                    item.get_TypeMeasuringInstrument())

##  Загружает архив, обновляет список работ и сбрасывает индекс выбора                                         
def full_load_refresh(window_main):
    load_jobs()
    window_main.select_index = None
    refresh_jobs_box_window_main(window_main)

##  Конвертирует в XML, добавляет СНИЛС и флаг Черновик/Отправлено    
def convert_to_xml_all(selected_object, window_main):
    jobs_list = read_jobs()
    if jobs_list is not None and selected_object is not None:
        mod_jobs = []
        switch_status = str(window_main.switch_status.get())
        print('Выбор черновика или нет: ', switch_status)
        full_status = window_main.full_enabled.get()
        print('Выбор свидетельства с шифром: ', full_status)

        for worker in selected_object:
            index_in_name_box = None
            work = False
            for item in jobs_list:
                if (worker.get_first() + worker.get_last() + worker.get_middle() ==
                    item.get_First() + item.get_Last() + item.get_Middle()):
                    mod_jobs.append(item)
                    item.set_TypeSaveMethod(switch_status)
                    item.set_SNILS(worker.get_SNILS())
                    work = True
            if not work:
                index_in_list = selected_object.index(worker)
                index_in_name_box = window_main.select_index[index_in_list]
                info = worker.get_last() + ' не работал' + '\nНе будет добавлен в XML'
                gui2.messagebox.showwarning(title='Внимательно!',
                                            message=info)
                window_main.name_box.select_clear(first=index_in_name_box)   
            print('Готово')
                    
        if mod_jobs:
            convert(mod_jobs, full_status)
        else:
            print('Совпадений не нашлось')

    else:
        print('Список деяний пуст')

##    Выход и удаление файла с работами
def exit_programm(window_main, options):
    options = options
    with open(options['path_to_file'], 'wb') as file:
        options['full_num_cert'] = window_main.full_enabled.get()
        options['draft_or_sent'] = window_main.switch_status.get()
        pickle.dump(options, file)
    del_jobs_file()
    window_main.main_window.destroy()
    
if __name__ == '__main__':
    main()             
