import unittest
from unittest.mock import MagicMock, patch

import requests

from src.HH_API import BaseApi, HeadHunterAPI


class TestBaseApi(unittest.TestCase):
    """Класс для проверки абстрактного класса"""
    def test_base_api_is_abstract(self):
        """Проверяем, что BaseApi действительно абстрактный класс"""
        with self.assertRaises(TypeError):
            BaseApi()


class TestHeadHunterAPI(unittest.TestCase):
    """Класс для проверки модуля API"""

    def setUp(self):
        self.api = HeadHunterAPI()

    def test_url_property_valid(self):
        """Проверяем, что url возвращает правильное значение"""
        self.assertEqual(self.api.url, "https://api.hh.ru/vacancies")

    def test_headers_property_valid(self):
        """Проверяем, что headers содержит User-Agent"""
        from config import USER_AGENT
        self.assertEqual(self.api.headers, {"User-Agent": USER_AGENT})

    def test_vacancies_property_valid(self):
        """Проверяем, что vacancies возвращает список"""
        self.assertEqual(self.api.vacancies, [])

    @patch('requests.get')
    def test_response_check_success(self, mock_get):
        """Проверяем успешную проверку ответа API"""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        self.assertTrue(self.api._HeadHunterAPI__response_check())

    @patch('requests.get')
    def test_response_check_failure(self, mock_get):
        """Проверяем неудачную проверку ответа API"""
        mock_get.side_effect = requests.exceptions.RequestException()

        self.assertFalse(self.api._HeadHunterAPI__response_check())

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Проверяем успешное получение вакансий"""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"items": [{"id": 1, "name": "Python Developer"}]}
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("Python")
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["name"], "Python Developer")

    @patch('requests.get')
    def test_get_vacancies_api_unavailable(self, mock_get):
        """Проверяем обработку недоступного API"""
        mock_get.side_effect = requests.exceptions.RequestException()

        with self.assertRaises(ConnectionError):
            self.api.get_vacancies("Python")

    @patch('requests.get')
    def test_get_vacancies_request_error(self, mock_get):
        """Проверяем обработку ошибки запроса"""

        mock_response_check = MagicMock()
        mock_response_check.raise_for_status.return_value = None
        mock_response_main = MagicMock()
        mock_response_main.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
        mock_get.side_effect = [mock_response_check, mock_response_main]

        with self.assertRaises(ValueError):
            self.api.get_vacancies("Python")


def test_url_property(hh_api):
    """Тест для свойства url"""

    assert hh_api.url == "https://api.hh.ru/vacancies"


def test_headers_property(hh_api):
    """Тест для свойства headers"""

    from config import USER_AGENT
    assert hh_api.headers == {"User-Agent": USER_AGENT}


def test_vacancies_property(hh_api):
    """Тест для свойства vacancies"""

    assert hh_api.vacancies == []
    test_vacancies = [{"id": 1, "name": "Test Vacancy"}]
    hh_api._HeadHunterAPI__vacancies = test_vacancies
    assert hh_api.vacancies == test_vacancies
