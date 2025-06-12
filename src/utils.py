import json
from typing import Dict, List


def json_load(filename: str) -> List[Dict]:
    """Функция для чтения json файла"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                return []
            return data
    except FileNotFoundError as error:
        print(f"Ошибка: файл {error.filename} не найден! ")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} содержит некорректный JSON! ")
        return []
