"""Модуль для работы с базой данных студентов.

Содержит модель данных Student и класс StudentDatabase для выполнения
CRUD операций с базой данных SQLite.
"""

import logging
from dataclasses import dataclass
from sqlite3 import Connection, connect

logger = logging.getLogger('StudentDatabase')

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
        
        logger.debug(f"Проверка существования студента с номером: {roll_number}")
        
        try:
            cursor = connection.cursor()
            sql = "SELECT 1 FROM student WHERE rno = ?"
            cursor.execute(sql, (roll_number,))
            exists = cursor.fetchone() is not None
            logger.debug(f"Студент с номером {roll_number} существует: {exists}")
            return exists
        except Exception as e:
            logger.error(f"Неожиданная ошибка при проверке существования студента: {str(e)}")
            raise     
    
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
        
        logger.info(f"Обновление студента: номер={student.roll_number}, имя={student.name}, оценка={student.marks}")
        
        connection = None
        try:
            connection = connect('datab.db')
            logger.debug("Соединение с базой данных установлено")
            
            if not StudentDatabase.check_student_exists(connection, student.roll_number):
                logger.warning(f"Студент с номером {student.roll_number} не найден")
                raise ValueError(f"Student with roll number {student.roll_number} not found")
            
            cursor = connection.cursor()
            sql = "UPDATE student SET name = ?, marks = ? WHERE rno = ?"
            cursor.execute(sql, (student.name, student.marks, student.roll_number))
            rows_affected = cursor.rowcount
            connection.commit()
            
            logger.info(f"Студент обновлен успешно. Затронуто строк: {rows_affected}")
            return True
            
        except ValueError as e:
            logger.error(f"Ошибка валидации при обновлении студента: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при обновлении студента: {str(e)}", exc_info=True)
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection:
                connection.close()
                logger.debug("Соединение с базой данных закрыто")
                          
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
        
        logger.info(f"Удаление студента с номером: {roll_number}")
        
        connection = None
        try:
            connection = connect('datab.db')
            logger.debug("Соединение с базой данных установлено")
        
            if not StudentDatabase.check_student_exists(connection, int(roll_number)):
                logger.warning(f"Студент с номером {roll_number} не найден")
                raise ValueError(f"Student with roll number {roll_number} not found")
        
            cursor = connection.cursor()
            sql = "DELETE FROM student WHERE rno = ?"
            cursor.execute(sql, (roll_number,))
            rows_deleted = cursor.rowcount
            connection.commit()
            
            logger.info(f"Студент удален успешно. Удалено строк: {rows_deleted}")
            return True
            
        except ValueError as e:
            logger.error(f"Ошибка валидации при удалении студента: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при удалении студента: {str(e)}", exc_info=True)
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection:
                connection.close()
                logger.debug("Соединение с базой данных закрыто")   
         
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
        
        logger.info(f"Сохранение нового студента: номер={student.roll_number}, имя={student.name}, оценка={student.marks}")
        
        connection = None
        try:
            connection = connect('datab.db')
            logger.debug("Соединение с базой данных установлено")
            
            cursor = connection.cursor()
            sql = "INSERT INTO student VALUES (?, ?, ?)"
            cursor.execute(sql, (student.roll_number, student.name, student.marks))
            connection.commit()
            
            logger.info(f"Студент сохранен успешно. ID: {student.roll_number}")
            return True
        except Exception as e:
            logger.error(f"Неожиданная ошибка при сохранении студента: {str(e)}", exc_info=True)
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection:
                connection.close()
                logger.debug("Соединение с базой данных закрыто")  
    
    @staticmethod
    def get_all_students() -> list[tuple[str, str, str]]:
        """Возвращает список всех студентов из базы данных.
        
        Returns:
            list[tuple[str, str, str]]: Список кортежей, где каждый кортеж
                содержит три строки: номер, имя и оценка студента.
        
        Raises:
            Exception: Если произошла ошибка при чтении данных из базы.
        """
        
        logger.debug("Запрос всех студентов из базы данных")
        
        connection = None
        try:
            connection = connect("datab.db")
            logger.debug("Соединение с базой данных установлено")
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM student")
            students = cursor.fetchall()
            
            logger.info(f"Получено {len(students)} студентов из базы данных")
            return students
            
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении студентов: {str(e)}", exc_info=True)
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection is not None:
                connection.close()
                logger.debug("Соединение с базой данных закрыто")
    
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
        
        logger.debug("Запрос студентов, отсортированных по оценкам")
        
        connection = None
        try:
            connection = connect("datab.db")
            logger.debug("Соединение с базой данных установлено")
            
            cursor = connection.cursor()
            cursor.execute("SELECT name, marks FROM student ORDER BY marks DESC")
            students = cursor.fetchall()
            
            logger.info(f"Получено {len(students)} студентов для сортировки по оценкам")
            return students
            
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении отсортированных студентов: {str(e)}", exc_info=True)
            raise Exception(f"Database error: {str(e)}")
        finally:
            if connection is not None:
                connection.close()
                logger.debug("Соединение с базой данных закрыто")