"""Главный модуль приложения для управления студентами.

Этот модуль содержит основной класс StudentManagementApp, который реализует
графический интерфейс и логику управления студентами, включая операции
добавления, обновления, удаления, просмотра и визуализации данных.
"""

import logging
from tkinter import END, INSERT, Button, Entry, Label, StringVar, Tk, Toplevel
from tkinter.messagebox import showerror, showinfo
from tkinter.scrolledtext import ScrolledText

import matplotlib.pyplot as plt

from api_service import ExternalAPIService
from data_base_service import Student, StudentDatabase
from validation_service import ValidationFunctions

logger = logging.getLogger('StudentManagement')

class StudentManagementApp:
    """Главный класс приложения для управления студентами.
    
    Класс объединяет графический интерфейс, бизнес-логику и управление окнами
    в единую систему. Реализует все основные операции CRUD для студентов,
    а также функции просмотра данных и визуализации.
    
    Attributes:
        FONT (tuple): Конфигурация шрифта для всех виджетов.
        WINDOW_SIZE (str): Размер окон приложения.
        PADDING_Y (int): Вертикальный отступ между виджетами.
        WIDTH (int): Ширина кнопок.
        location (str): Текущая геолокация, полученная из API.
        temperature (str): Текущая температура, полученная из API.
        main_window (Tk): Главное окно приложения.
        add_window (Toplevel): Окно добавления студента.
        view_window (Toplevel): Окно просмотра студентов.
        update_window (Toplevel): Окно обновления студента.
        delete_window (Toplevel): Окно удаления студента.
        st_rno (StringVar): Переменная для хранения номера студента.
        st_nme (StringVar): Переменная для хранения имени студента.
        st_mks (StringVar): Переменная для хранения оценок студента.
    """
    
    def __init__(self):
        """Инициализирует приложение, создавая окна и получая внешние данные."""
        
        logger.info("Инициализация приложения StudentManagementApp")
        
        self.FONT = ("Calibri", 20, "bold")
        self.WINDOW_SIZE = "600x600+400+100"
        self.PADDING_Y = 10
        self.WIDTH = 10
        
        
        try:
            logger.debug("Получение данных о местоположении и температуре")
            self.location = ExternalAPIService.fetch_location()
            self.temperature = ExternalAPIService.fetch_temperature()
            logger.info(f"Данные получены: location={self.location}, temperature={self.temperature}")
        except Exception as e:
            logger.error(f"Ошибка при получении внешних данных", exc_info=True)
            self.location = "Unknown"
            self.temperature = "Unknown"
        
        self.setup_main_window()
        self.setup_add_window()
        self.setup_view_window()
        self.setup_update_window()
        self.setup_delete_window()
        
        logger.info("Приложение успешно инициализировано")
    
    def setup_main_window(self):
        """Создает и настраивает главное окно приложения.
        
        Инициализирует главное окно, создает кнопки для навигации
        и информационные метки с данными о местоположении и температуре.
        """
        
        logger.debug("Настройка главного окна приложения")
        
        self.main_window = Tk()
        self.main_window.geometry(self.WINDOW_SIZE)
        self.main_window.title("Student Management System")
        
        self.st_rno = StringVar()
        self.st_nme = StringVar()
        self.st_mks = StringVar()
        
        btn_add = Button(
            self.main_window, 
            text="Add", 
            font=self.FONT, 
            width=self.WIDTH, 
            command=self.show_add_window
        )
        btn_view = Button(
            self.main_window, 
            text="View", 
            font=self.FONT, 
            width=self.WIDTH, 
            command=self.view_entries
        )
        btn_update = Button(
            self.main_window, 
            text="Update", 
            font=self.FONT, 
            width=self.WIDTH, 
            command=self.show_update_window
        )
        btn_delete = Button(
            self.main_window, 
            text="Delete", 
            font=self.FONT, 
            width=self.WIDTH, 
            command=self.show_delete_window
        )
        btn_charts = Button(
            self.main_window, 
            text="Charts", 
            font=self.FONT, 
            width=self.WIDTH, 
            command=self.display_students_chart
        )
        
        lbl_location = Label(self.main_window, text="Location: ", font=self.FONT)
        lbl_location_value = Label(self.main_window, text=self.location, font=self.FONT)
        lbl_temperature = Label(self.main_window, text="Temperature: ", font=self.FONT)
        lbl_temperature_value = Label(self.main_window, text=self.temperature, font=self.FONT)
        
        btn_add.pack(pady=self.PADDING_Y)
        btn_view.pack(pady=self.PADDING_Y)
        btn_update.pack(pady=self.PADDING_Y)
        btn_delete.pack(pady=self.PADDING_Y)
        btn_charts.pack(pady=self.PADDING_Y)
        
        lbl_location.place(x=5, y=500, anchor='sw')
        lbl_temperature.place(x=350, y=500, anchor='sw')
        lbl_location_value.place(x=111, y=500, anchor='sw')
        lbl_temperature_value.place(x=510, y=500, anchor='sw')
        
        logger.debug("Главное окно настроено")
    
    def setup_add_window(self):
        """Создает окно для добавления нового студента.
        
        Создает форму с полями ввода для номера, имени и оценок студента,
        а также кнопки для сохранения данных и возврата в главное меню.
        """
        
        self.add_window = Toplevel(self.main_window)
        self.add_window.title("Add Student")
        self.add_window.geometry(self.WINDOW_SIZE)
        
        add_lbl_rno = Label(self.add_window, text="Enter roll no", font=self.FONT)
        self.add_ent_rno = Entry(self.add_window, bd=5, font=self.FONT, textvariable=self.st_rno)
        
        add_lbl_name = Label(self.add_window, text="Enter name", font=self.FONT)
        self.add_ent_name = Entry(self.add_window, bd=5, font=self.FONT, textvariable=self.st_nme)
        
        add_lbl_marks = Label(self.add_window, text="Enter marks", font=self.FONT)
        self.add_ent_marks = Entry(self.add_window, bd=5, font=self.FONT, textvariable=self.st_mks)
        
        add_btn_save = Button(
            self.add_window, 
            text="Save", 
            width=self.WIDTH,
            font=self.FONT, 
            command=self.create_entry
        )
        add_btn_back = Button(
            self.add_window, 
            text="Back", 
            width=self.WIDTH,
            font=self.FONT, 
            command=self.hide_add_window
        )
        
        add_lbl_rno.pack(pady=self.PADDING_Y)
        self.add_ent_rno.pack(pady=self.PADDING_Y)
        add_lbl_name.pack(pady=self.PADDING_Y)
        self.add_ent_name.pack(pady=self.PADDING_Y)
        add_lbl_marks.pack(pady=self.PADDING_Y)
        self.add_ent_marks.pack(pady=self.PADDING_Y)
        add_btn_save.pack(pady=self.PADDING_Y)
        add_btn_back.pack(pady=self.PADDING_Y)
        
        self.add_window.withdraw()
    
    def setup_view_window(self):
        """Создает окно для просмотра списка всех студентов.
        
        Инициализирует текстовое поле с прокруткой для отображения
        данных о студентах и кнопку для возврата в главное меню.
        """
        
        self.view_window = Toplevel(self.main_window)
        self.view_window.title("View Students")
        self.view_window.geometry(self.WINDOW_SIZE)
        
        self.view_st_data = ScrolledText(
            self.view_window, 
            width=30, 
            height=10, 
            font=self.FONT
        )
        view_btn_back = Button(
            self.view_window, 
            text="Back", 
            width=self.WIDTH, 
            font=self.FONT, 
            command=self.hide_view_window
        )
        
        self.view_st_data.pack(pady=self.PADDING_Y)
        view_btn_back.pack(pady=self.PADDING_Y)
        
        self.view_window.withdraw()
    
    def setup_update_window(self):
        """Создает окно для обновления данных существующего студента.
        
        Создает форму с полями ввода, аналогичную окну добавления,
        но предназначенную для изменения информации о существующем студенте.
        """
        
        self.update_window = Toplevel(self.main_window)
        self.update_window.title("Update Student")
        self.update_window.geometry(self.WINDOW_SIZE)
        
        update_lbl_rno = Label(self.update_window, text="Enter roll no", font=self.FONT)
        self.update_ent_rno = Entry(self.update_window, bd=5, font=self.FONT, textvariable=self.st_rno)
        
        update_lbl_name = Label(self.update_window, text="Enter name", font=self.FONT)
        self.update_ent_name = Entry(self.update_window, bd=5, font=self.FONT, textvariable=self.st_nme)
        
        update_lbl_marks = Label(self.update_window, text="Enter marks", font=self.FONT)
        self.update_ent_marks = Entry(self.update_window, bd=5, font=self.FONT, textvariable=self.st_mks)
        
        update_btn_save = Button(
            self.update_window, 
            text="Save", 
            width=self.WIDTH,
            font=self.FONT, 
            command=self.update_entry
        )
        update_btn_back = Button(
            self.update_window, 
            text="Back", 
            width=self.WIDTH,
            font=self.FONT, 
            command=self.hide_update_window
        )
        
        update_lbl_rno.pack(pady=self.PADDING_Y)
        self.update_ent_rno.pack(pady=self.PADDING_Y)
        update_lbl_name.pack(pady=self.PADDING_Y)
        self.update_ent_name.pack(pady=self.PADDING_Y)
        update_lbl_marks.pack(pady=self.PADDING_Y)
        self.update_ent_marks.pack(pady=self.PADDING_Y)
        update_btn_save.pack(pady=self.PADDING_Y)
        update_btn_back.pack(pady=self.PADDING_Y)
        
        self.update_window.withdraw()
    
    def setup_delete_window(self):
        """Создает окно для удаления студента из базы данных.
        
        Создает форму с одним полем ввода для номера студента
        и кнопками для подтверждения удаления и возврата в главное меню.
        """
        
        self.delete_window = Toplevel(self.main_window)
        self.delete_window.title("Delete Student")
        self.delete_window.geometry(self.WINDOW_SIZE)
        
        delete_lbl_rno = Label(self.delete_window, text="Enter roll no ", font=self.FONT)
        self.delete_ent_rno = Entry(self.delete_window, bd=5, font=self.FONT, textvariable=self.st_rno)
        
        delete_btn_delete = Button(
            self.delete_window, 
            text="Delete", 
            width=self.WIDTH, 
            font=self.FONT, 
            command=self.delete_entry
        )
        delete_btn_back = Button(
            self.delete_window, 
            text="Back", 
            width=self.WIDTH, 
            font=self.FONT, 
            command=self.hide_delete_window
        )
        
        delete_lbl_rno.pack(pady=self.PADDING_Y)
        self.delete_ent_rno.pack(pady=self.PADDING_Y)
        delete_btn_delete.pack(pady=self.PADDING_Y)
        delete_btn_back.pack(pady=self.PADDING_Y)
        
        self.delete_window.withdraw()
    
    def create_entry(self):
        """Обрабатывает добавление нового студента в базу данных.
        
        Получает данные из полей ввода, выполняет валидацию,
        создает объект Student и сохраняет его в базе данных.
        При успешном сохранении очищает поля и закрывает окно добавления.
        
        Raises:
            ValueError: Если валидация данных не пройдена.
            Exception: Если произошла ошибка при работе с базой данных.
        """
        
        logger.info("Запуск процесса добавления студента")
        
        try:
            roll_number = self.st_rno.get()
            name = self.st_nme.get()
            marks = self.st_mks.get()
            
            logger.debug(f"Получены данные для добавления: "
                         f"froll={roll_number}, name={name}, marks={marks}")
            
            error = ValidationFunctions.validate_student(roll_number, name, marks)
            if error:
                logger.warning(f"Валидация не пройдена: {error}")
                raise ValueError(error)
            
            student = Student(int(roll_number), name, int(marks))
            logger.info(f"Создан объект студента: {student}")
            
            StudentDatabase.save_student_in_db(student)
            logger.info(f"Студент успешно сохранен в БД: {student}")
            
            showinfo('Success', 'Record added')
            logger.info("Пользователю показано сообщение об успехе")
            
            self.clear_fields()
            self.hide_add_window()
            logger.debug("Поля очищены, окно добавления закрыто")
            
        except ValueError as e:
            logger.error(f"Ошибка валидации при добавлении студента", exc_info=True)
            showerror('Failure', str(e))
        except Exception as e:
            logger.error(f"Критическая ошибка при добавлении студента", exc_info=True)
            showerror('Failure', str(e))
    
    def update_entry(self):
        """Обрабатывает обновление данных существующего студента.
        
        Получает обновленные данные из полей ввода, выполняет валидацию,
        создает объект Student и обновляет соответствующую запись в базе данных.
        При успешном обновлении очищает поля и закрывает окно.
        
        Raises:
            ValueError: Если валидация данных не пройдена.
            Exception: Если произошла ошибка при работе с базой данных.
        """
        
        logger.info("Запуск процесса обновления студента")
        
        try:
            roll_number = self.st_rno.get()
            name = self.st_nme.get()
            marks = self.st_mks.get()
            
            logger.debug(f"Получены данные для обновления: "
                         f"roll={roll_number}, name={name}, marks={marks}")
            
            error = ValidationFunctions.validate_student(roll_number, name, marks)
            if error:
                logger.warning(f"Валидация не пройдена: {error}")
                raise ValueError(error)
            
            student = Student(int(roll_number), name, int(marks))
            logger.info(f"Обновление студента: {student}")
            
            StudentDatabase.update_student_in_db(student)
            logger.info(f"Студент успешно обновлен в БД: {student}")
            
            showinfo('Success', 'Record updated')
            
            self.clear_fields()
            self.hide_update_window()
            
        except ValueError as e:
            logger.error(f"Ошибка валидации при обновлении студента", exc_info=True)
            showerror('Failure', str(e))
        except Exception as e:
            logger.error(f"Критическая ошибка при обновлении студента", exc_info=True)
            showerror('Failure', str(e))
    
    def delete_entry(self):
        """Обрабатывает удаление студента из базы данных.
        
        Получает номер студента из поля ввода, выполняет валидацию номера
        и удаляет соответствующую запись из базы данных.
        При успешном удалении очищает поле и закрывает окно.
        
        Raises:
            ValueError: Если валидация номера не пройдена.
            Exception: Если произошла ошибка при работе с базой данных.
        """
        
        logger.info("Запуск процесса удаления студента")
        
        try: 
            roll_number = self.st_rno.get()
            logger.debug(f"Получен номер студента для удаления: {roll_number}")
            
            error = ValidationFunctions.validate_integer("Roll number", roll_number)
            if error:
                logger.warning(f"Валидация номера не пройдена: {error}")
                raise ValueError(error)
            
            logger.info(f"Удаление студента с номером: {roll_number}")
            
            StudentDatabase.delete_student_in_db(roll_number)
            logger.info(f"Студент с номером {roll_number} успешно удален")
            
            showinfo("Success", "Record deleted")
            
            self.clear_fields()
            self.hide_delete_window()
            
        except ValueError as e:
            logger.error(f"Ошибка валидации при удалении студента", exc_info=True)
            showerror("Error", str(e))
        except Exception as e:
            logger.error(f"Критическая ошибка при удалении студента", exc_info=True)
            showerror("Error", str(e))
    
    def view_entries(self):
        """Отображает список всех студентов в окне просмотра.
        
        Загружает данные всех студентов из базы данных, форматирует их
        в читаемый вид и отображает в текстовом поле с прокруткой.
        При ошибке загрузки данных возвращается в главное окно.
        
        Raises:
            Exception: Если произошла ошибка при загрузке данных из базы.
        """
        
        logger.info("Запуск процесса просмотра студентов")
        
        try:
            self.view_window.deiconify()
            self.main_window.withdraw()
            self.view_st_data.delete(1.0, END)
            logger.debug("Окно просмотра активировано")
            
            data = StudentDatabase.get_all_students()
            logger.debug(f"Получено {len(data)} записей из БД")
            
            if not data:
                info = "No students found"
                logger.info("В базе данных нет студентов")
            else:
                info = ""
                for d in data:
                    info += f"Rno: {d[0]}\tName: {d[1]}\tMarks: {d[2]}\n"
                logger.debug(f"Сформирован текст для отображения длиной {len(info)} символов")
            
            self.view_st_data.insert(INSERT, info)
            logger.info("Данные успешно отображены в окне просмотра")
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных студентов", exc_info=True)
            showerror("Error", str(e))
            self.main_window.deiconify()
            self.view_window.withdraw()
    
    def display_students_chart(self):
        """Создает и отображает столбчатую диаграмму успеваемости студентов.
        
        Загружает данные студентов, отсортированные по оценкам,
        и создает столбчатую диаграмму с помощью библиотеки matplotlib.
        Каждому студенту соответствует столбец, высота которого
        соответствует его оценке.
        
        Raises:
            Exception: Если произошла ошибка при создании графика.
        """
        
        logger.info("Запуск создания диаграммы успеваемости")
        
        try:
            data = StudentDatabase.get_students_sorted_by_marks()
            logger.debug(f"Получено {len(data)} записей для диаграммы")
            
            if not data:
                logger.warning("Нет данных для построения диаграммы")
                showerror("Info", "No data for chart")
                return
            
            cnames = [x[0] for x in data]
            cmarks = [x[1] for x in data]
            
            logger.debug(f"Данные для диаграммы: имена={cnames}, оценки={cmarks}")
            
            plt.bar(cnames, cmarks, color=('red', 'green', 'blue', 'yellow'))
            plt.xlabel("Names")
            plt.ylabel("Marks")
            plt.title("Student Marks")
            plt.show()
            
            logger.info("Диаграмма успешно создана и отображена")
            
        except Exception as e:
            logger.error(f"Ошибка при создании диаграммы", exc_info=True)
            showerror("Error", f"Failed to display chart: {str(e)}")
    
    def show_add_window(self):
        """Отображает окно добавления студента и скрывает главное окно."""
        
        self.clear_fields()
        self.add_window.deiconify()
        self.main_window.withdraw()
    
    def hide_add_window(self):
        """Скрывает окно добавления студента и отображает главное окно."""
        
        self.main_window.deiconify()
        self.add_window.withdraw()
    
    def show_view_window(self):
        """Отображает окно просмотра студентов и скрывает главное окно."""
        
        self.view_window.deiconify()
        self.main_window.withdraw()
    
    def hide_view_window(self):
        """Скрывает окно просмотра студентов и отображает главное окно."""
        
        self.main_window.deiconify()
        self.view_window.withdraw()
    
    def show_update_window(self):
        """Отображает окно обновления студента и скрывает главное окно."""
        
        self.update_window.deiconify()
        self.main_window.withdraw()
    
    def hide_update_window(self):
        """Скрывает окно обновления студента и отображает главное окно."""
        
        self.main_window.deiconify()
        self.update_window.withdraw()
    
    def show_delete_window(self):
        """Отображает окно удаления студента и скрывает главное окно."""
        
        self.delete_window.deiconify()
        self.main_window.withdraw()
    
    def hide_delete_window(self):
        """Скрывает окно удаления студента и отображает главное окно."""
        
        self.main_window.deiconify()
        self.delete_window.withdraw()
    
    def clear_fields(self):
        """Очищает значения всех переменных полей ввода в приложении."""
        
        logger.debug("Очистка полей ввода")
        self.st_rno.set("")
        self.st_nme.set("")
        self.st_mks.set("")
    
    def run(self):
        """Запускает главный цикл обработки событий приложения."""
        
        logger.info("Запуск главного цикла приложения")
        self.main_window.mainloop()
        logger.info("Приложение завершено")


if __name__ == "__main__":
    """Точка входа в приложение. Создает экземпляр StudentManagementApp и запускает его."""
    
    app = StudentManagementApp()
    app.run()