"""Модуль для работы с базой данных студентов.

Содержит модель данных Student и класс StudentDatabase для выполнения
CRUD операций с базой данных SQLite.
"""

from dataclasses import dataclass
from sqlite3 import Connection, connect


@dataclass
class Student:
    """Модель данных студента.
    
    Attributes:
        roll_number (int): Уникальный номер студента.
        name (str): Полное имя студента.
        marks (int): Оценка студента.
    """
    
    roll_number: int
    name: str
    marks: int


class StudentDatabase:
    """Класс для выполнения операций с базой данных студентов.
    
    Предоставляет статические методы для выполнения основных CRUD операций
    с таблицей 'student' в базе данных SQLite. Все методы включают обработку
    исключений и управление соединениями с базой данных.
    
    Methods:
        check_student_exists: Проверяет существование студента по номеру.
        update_student_in_db: Обновляет данные существующего студента.
        delete_student_in_db: Удаляет студента из базы данных.
        save_student_in_db: Сохраняет нового студента в базу данных.
        get_all_students: Возвращает список всех студентов.
        get_students_sorted_by_marks: Возвращает студентов, отсортированных по оценкам.
    """
    
    @staticmethod
    def check_student_exists(connection: Connection, roll_number: int) -> bool:
        """Проверяет существование студента с заданным номером.
        
        Args:
            connection (Connection): Активное соединение с базой данных.
            roll_number (int): Номер студента для проверки.
        
        Returns:
            bool: True если студент существует, иначе False.
        """
        
        cursor = connection.cursor()
        sql = "SELECT 1 FROM student WHERE rno = ?"
        cursor.execute(sql, (roll_number,))
        return cursor.fetchone() is not None      
    
    @staticmethod    
    def update_student_in_db(student: Student) -> bool:
        """Обновляет данные существующего студента в базе данных.
        
        Args:
            student (Student): Объект студента с обновленными данными.
        
        Returns:
            bool: True если обновление выполнено успешно.
        
        Raises:
            ValueError: Если студент с указанным номером не найден.
            Exception: Если произошла ошибка при работе с базой данных.
        """
        
        connection = None
        try:
            connection = connect('datab.db')
            
            if not StudentDatabase.check_student_exists(connection, student.roll_number):
                raise ValueError(f"Student with roll number "
                                 f"{student.roll_number} not found")
            
            cursor = connection.cursor()
            sql = "UPDATE student SET name = ?, marks = ? WHERE rno = ?"
            cursor.execute(sql, (student.name, student.marks, student.roll_number))
            connection.commit()
            
            return True
        except ValueError:
            raise
        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection:
                connection.close()
                          
    @staticmethod  
    def delete_student_in_db(roll_number: str) -> bool:
        """Удаляет студента из базы данных по номеру.
        
        Args:
            roll_number (str): Номер студента для удаления.
        
        Returns:
            bool: True если удаление выполнено успешно.
        
        Raises:
            ValueError: Если студент с указанным номером не найден.
            Exception: Если произошла ошибка при работе с базой данных.
        """
        
        connection = None
        try:
            connection = connect('datab.db')
        
            if not StudentDatabase.check_student_exists(connection, int(roll_number)):
                raise ValueError(f"Student with roll number "
                                 f"{roll_number} not found")
        
            cursor = connection.cursor()
            sql = "DELETE FROM student WHERE rno = ?"
            cursor.execute(sql, (roll_number,))
            connection.commit()
        
            return True
        except ValueError:
            raise
        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection:
                connection.close()        
         
    @staticmethod  
    def save_student_in_db(student: Student) -> bool:
        """Сохраняет нового студента в базу данных.
        
        Args:
            student (Student): Объект студента для сохранения.
        
        Returns:
            bool: True если сохранение выполнено успешно.
        
        Raises:
            Exception: Если произошла ошибка при работе с базой данных.
        """
        
        connection = None
        try:
            connection = connect('datab.db')
            cursor = connection.cursor()
            sql = "INSERT INTO student VALUES (?, ?, ?)"
            cursor.execute(sql, (student.roll_number,
                                 student.name,
                                 student.marks))
            connection.commit()
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection:
                connection.close()        
    
    @staticmethod
    def get_all_students() -> list[tuple[str, str, str]]:
        """Возвращает список всех студентов из базы данных.
        
        Returns:
            list[tuple[str, str, str]]: Список кортежей, где каждый кортеж
                содержит три строки: номер, имя и оценка студента.
        
        Raises:
            Exception: Если произошла ошибка при чтении данных из базы.
        """
        
        connection = None
        try:
            connection = connect("datab.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM student")
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection is not None:
                connection.close()
    
    @staticmethod
    def get_students_sorted_by_marks() -> list[tuple[str, str, str]]:
        """Возвращает студентов, отсортированных по убыванию оценок.
        
        Returns:
            list[tuple[str, str, str]]: Список кортежей, где каждый кортеж
                содержит две строки: имя и оценка студента, отсортированные
                по оценкам в порядке убывания.
        
        Raises:
            Exception: Если произошла ошибка при чтении данных из базы.
        """
        
        connection = None
        try:
            connection = connect("datab.db")
            cursor = connection.cursor()
            cursor.execute("SELECT name, marks FROM student ORDER BY marks DESC")
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection is not None:
                connection.close()