"""Конфигурация логирования для приложения управления студентами."""

import logging
import logging.handlers
from datetime import datetime
import os

def setup_logging():
    """Настройка системы логирования для приложения."""
    
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    logger = logging.getLogger('StudentManagement')
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    log_file = os.path.join(log_dir, f'student_management_{datetime.now().strftime("%Y-%m-%d")}.log')
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when='midnight', interval=1, backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    error_handler = logging.FileHandler(os.path.join(log_dir, 'errors.log'))
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(log_format, datefmt=date_format)
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)
    
    db_logger = logging.getLogger('StudentDatabase')
    db_logger.setLevel(logging.DEBUG)
    
    api_logger = logging.getLogger('ExternalAPI')
    api_logger.setLevel(logging.INFO)
    
    validation_logger = logging.getLogger('Validation')
    validation_logger.setLevel(logging.DEBUG)
    
    logger.info("Система логирования инициализирована")
    return logger