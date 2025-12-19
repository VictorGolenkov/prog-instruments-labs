"""Модуль валидации данных для приложения управления студентами.

Содержит класс ValidationFunctions со статическими методами для проверки
корректности вводимых данных, таких как числовые значения, строки и комплексные
данные студента.
"""

import logging

logger = logging.getLogger('Validation')

class ValidationFunctions:
    """Класс, предоставляющий методы валидации для данных приложения.
    
    Все методы класса являются статическими и возвращают строки с описанием
    ошибок. Пустая строка возвращается при успешной валидации.
    
    Methods:
        validate_integer: Проверяет корректность целочисленного значения.
        validate_string: Проверяет корректность строкового значения.
        validate_student: Проверяет корректность всех полей студента.
    """
    
    @staticmethod
    def validate_integer(field_name: str, field_value: str) -> str:
        """Проверяет корректность целочисленного значения.
        
        Выполняет три проверки:
        1. Поле не должно быть пустым
        2. Поле должно содержать только цифры
        3. Число должно быть больше 0
        
        Args:
            field_name (str): Название проверяемого поля (для сообщений об ошибках).
            field_value (str): Значение поля в виде строки.
        
        Returns:
            str: Пустую строку при успешной валидации, иначе строку с описанием ошибки.
        """
        
        logger.debug(f"Валидация целого числа: поле={field_name}, значение={field_value}")
        
        if not field_value:
            logger.warning(f"Поле '{field_name}' не может быть пустым")
            return f"{field_name} should not be empty"
        
        if not field_value.isdigit():
            logger.warning(f"Поле '{field_name}' должно содержать только цифры: '{field_value}'")
            return f"{field_name} should contain only digits"
        
        if int(field_value) < 1:
            logger.warning(f"Поле '{field_name}' должно быть больше 0: '{field_value}'")
            return f"{field_name} should be greater than 0"
        
        logger.debug(f"Валидация поля '{field_name}' прошла успешно")
        return ""
        
    @staticmethod    
    def validate_string(field_name: str, field_value: str) -> str:
        """Проверяет корректность строкового значения.
        
        Выполняет три проверки:
        1. Поле не должно быть пустым
        2. Поле должно содержать только буквенные символы (после удаления пробелов)
        3. Длина строки (после удаления пробелов) должна быть не менее 2 символов
        
        Args:
            field_name (str): Название проверяемого поля (для сообщений об ошибках).
            field_value (str): Значение поля в виде строки.
        
        Returns:
            str: Пустую строку при успешной валидации, иначе строку с описанием ошибки.
        """
        
        logger.debug(f"Валидация строки: поле={field_name}, значение='{field_value}'")
        
        if not field_value:
            logger.warning(f"Поле '{field_name}' не может быть пустым")
            return f"{field_name} should not be empty"
        
        stripped_value = field_value.strip()
        
        if not stripped_value.isalpha():
            logger.warning(f"Поле '{field_name}' должно содержать только буквы: '{field_value}'")
            return f"{field_name} should contain only characters"
        
        if len(stripped_value) < 2:
            logger.warning(f"Поле '{field_name}' должно быть не менее 2 символов: '{field_value}'")
            return f"{field_name} should be at least 2 characters long"
        
        logger.debug(f"Валидация поля '{field_name}' прошла успешно")
        return ""
    
    @staticmethod
    def validate_student(roll_str: str, name_str: str, marks_str: str) -> str:
        """Выполняет комплексную валидацию данных студента.
        
        Проверяет корректность трех полей студента:
        1. Номер студента (целое число больше 0)
        2. Имя студента (непустая строка только из букв, длина ≥ 2)
        3. Оценка студента (целое число больше 0)
        
        Args:
            roll_str (str): Строковое представление номера студента.
            name_str (str): Имя студента.
            marks_str (str): Строковое представление оценки студента.
        
        Returns:
            str: Пустую строку при успешной валидации всех полей,
                иначе строку с описанием первой обнаруженной ошибки.
        
        Note:
            Валидация выполняется для всех полей, но возвращается только
            первая обнаруженная ошибка. Порядок проверки: номер, имя, оценка.
        """
        
        logger.debug(f"Комплексная валидация студента: roll={roll_str}, name='{name_str}', marks={marks_str}")
        
        roll_error = ValidationFunctions.validate_integer("Roll number", roll_str)
        if roll_error:
            logger.warning(f"Ошибка валидации номера студента: {roll_error}")
            return roll_error
        
        name_error = ValidationFunctions.validate_string("Name", name_str)
        if name_error:
            logger.warning(f"Ошибка валидации имени студента: {name_error}")
            return name_error
        
        marks_error = ValidationFunctions.validate_integer("Marks", marks_str)
        if marks_error:
            logger.warning(f"Ошибка валидации оценок студента: {marks_error}")
            return marks_error
        
        logger.info("Все поля студента прошли валидацию успешно")
        return ""