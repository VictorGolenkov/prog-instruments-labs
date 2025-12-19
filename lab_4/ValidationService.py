"""Модуль валидации данных для приложения управления студентами.

Содержит класс ValidationFunctions со статическими методами для проверки
корректности вводимых данных, таких как числовые значения, строки и комплексные
данные студента.
"""

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
        
        if not field_value:
            return f"{field_name} should not be empty"
        if not field_value.isdigit():
            return f"{field_name} should contain only digits"
        if int(field_value) < 1:
            return f"{field_name} should be greater than 0"
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
        
        if not field_value:
            return f"{field_name} should not be empty"
        if not field_value.strip().isalpha():
            return f"{field_name} can contain only characters"
        if len(field_value.strip()) < 2:
            return f"{field_name} be at least 2 characters long"
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
        
        roll_error = ValidationFunctions.validate_integer("Roll number", roll_str)
        name_error = ValidationFunctions.validate_string("Name", name_str)
        marks_error = ValidationFunctions.validate_integer("Marks", marks_str)
        
        if roll_error:
            return roll_error
        if name_error:
            return name_error
        if marks_error:
            return marks_error
        
        return ""