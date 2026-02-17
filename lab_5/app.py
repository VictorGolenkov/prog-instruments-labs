"""Точка входа приложения управления студентами с логированием."""

import os
import sys

from lab_5.gui import StudentManagementApp
from logger_config import setup_logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Главная функция запуска приложения."""
    
    logger = setup_logging()
    
    try:
        logger.info("Запуск приложения управления студентами")
        
        app = StudentManagementApp()
        app.run()
        
        logger.info("Приложение успешно завершено")
        
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске приложения", exc_info=True)
        print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()