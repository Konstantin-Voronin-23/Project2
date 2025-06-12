import unittest
import json
import os
from typing import List, Dict
from src.utils import json_load


class TestJsonLoad(unittest.TestCase):
    """Класс для тестирования модуля utils"""
    def setUp(self):
        """Создаем временные файлы для тестирования"""

        self.valid_json = 'valid.json'
        with open(self.valid_json, 'w', encoding='utf-8') as f:
            json.dump([{"id": 1, "amount": 100}], f)

        self.empty_json = 'empty.json'
        with open(self.empty_json, 'w', encoding='utf-8') as f:
            f.write('')

        self.invalid_json = 'invalid.json'
        with open(self.invalid_json, 'w', encoding='utf-8') as f:
            f.write('{"id": 1, "amount": 100')

        self.not_list_json = 'not_list.json'
        with open(self.not_list_json, 'w', encoding='utf-8') as f:
            json.dump({"id": 1, "amount": 100}, f)

    def tearDown(self):
        """Удаляем временные файлы после тестов"""
        for filename in [self.valid_json, self.empty_json,
                         self.invalid_json, self.not_list_json]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_load_valid_json(self):
        """Тест загрузки корректного JSON файла"""
        result = json_load(self.valid_json)
        self.assertEqual(result, [{"id": 1, "amount": 100}])

    def test_load_nonexistent_file(self):
        """Тест загрузки несуществующего файла"""
        result = json_load('nonexistent.json')
        self.assertEqual(result, [])

    def test_load_invalid_json(self):
        """Тест загрузки некорректного JSON"""
        result = json_load(self.invalid_json)
        self.assertEqual(result, [])

    def test_load_empty_file(self):
        """Тест загрузки пустого файла"""
        result = json_load(self.empty_json)
        self.assertEqual(result, [])

    def test_load_not_list_json(self):
        """Тест загрузки JSON, который не является списком"""
        result = json_load(self.not_list_json)
        self.assertEqual(result, [])
