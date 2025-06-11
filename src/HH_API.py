from abc import ABC, abstractmethod
import requests


class Base_Api(ABC):
    """Базовый абстрактный класс для подключения к API"""

    @abstractmethod
    def _connect(self):
        """Абстрактный метод для подключения к API"""

        pass

    @abstractmethod
    def load_vacancies(self, keyword, amount):
        """Абстроктный метод для получения вакансий по ключевому слову"""

        pass


class HeadHunterAPI(Base_Api):
    """Класс для подключения к API сайта HeadHunter"""

    BASE_URL = 'https://api.hh.ru/vacancies'

    def __init__(self):
        """Метод иниуиализации"""
        self.__session = None

    def _connect(self):
        """Абстрактный метод для подключения к API"""

        self.__session = requests.Session()
        response = self.__session.get(self.BASE_URL)
        response.raise_for_status()
        return response


    def load_vacancies(self, keyword, amount):
        """Абстроктный метод для получения вакансий по ключевому слову"""

        self._connect()

        params = {
            'text': keyword,
            'per_page': amount,
            'page': 1,
            'area': 1
        }

        response = self.__session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        vacancies = response.json().get('items', [])

        return [
            {
                'name': vacancy['name'],
                'salary': vacancy['salary'],
                'url': vacancy['url'],
                'description': vacancy['snippet']['responsibility'],
                'city': vacancy['area']['name']

            }
            for vacancy in vacancies
        ]
