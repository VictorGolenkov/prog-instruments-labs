import json
from typing import Any, Dict

def read_txt(file_name: str) -> str:
    """Считывает текcт из .txt файла

    Args:
        file_name (str): Путь к файлу

    Returns:
        str: Содержимое файла
    """
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            text: str = f.read()
            return text
    except Exception as e:
        print(f"Error: {e}")
        return ""
    
def save_txt(file_name: str, text: str):
    """Удаляет содержимое файла и сохраняет в нём новый текст.
    Если файла не существует, создаёт его.

    Args:
        file_name (str): Путь к файлу
        text (str): Текст, который необходимо сохранить
    """
    try:
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Error: {e}")
        
def read_json(file_name: str) -> Dict[str, Any]:
    """Считывает данные из .json файла

    Args:
        file_name (str): Путь к файлу

    Returns:
        Dict[str, Any]: Словарь объектов, содеражавшихся в .json файле
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return(json.load(f))
    except Exception as e:
        print(f"Error: {e}")
        return {}
    
def save_json(file_name: str, data: dict[str, Any]):
    """Удаляет содержимое файла и сохраняет в нём новые данных.
    Если файла не существует, создаёт его.

    Args:
        file_name (str): Путь к файлу
        text (str): Словарь, который необходимо сохранить
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {e}")