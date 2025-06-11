import json
from typing import Dict, List


def read_json_file(filename: str) -> List[Dict]:
    """Функция для чтения json файла с операциями транзакций"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                return []
            return data
    except FileNotFoundError as error:
        print(f"Ошибка: файл {error.filename} не найден! ")
        return []
    except json.JSONDecodeError as error:
        print(f"Ошибка: файл {filename} содержит некорректный JSON! ")
        return []
