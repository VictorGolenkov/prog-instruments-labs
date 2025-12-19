"""Точка входа приложения управления студентами с логированием."""

import sys
import os

# Добавляем текущую директорию в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from LoggerConfig import setup_logging

def main():
    """Главная функция запуска приложения."""
    
    logger = setup_logging()
    
    try:
        logger.info("Запуск приложения управления студентами")
        
        from GUI import StudentManagementApp
        
        app = StudentManagementApp()
        app.run()
        
        logger.info("Приложение успешно завершено")
        
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске приложения: {str(e)}", exc_info=True)
        print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()