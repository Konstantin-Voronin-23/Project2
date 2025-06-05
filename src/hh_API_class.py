from abc import ABC, abstractmethod
import requests


class Base_Api(ABC):
    """Базовый абстрактный класс для подключения к API"""

    @abstractmethod
    def _connect(self):
        """Абстрактный метод для подключения к API"""

        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int, page: int):
        """Абстроктный метод для получения вакансий по ключевому слову"""

        pass


class Hh_Api(Base_Api):
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


    def get_vacancies(self, keyword: str, per_page: int, page: int):
        """Абстроктный метод для получения вакансий по ключевому слову"""

        self._connect()

        params = {
            'text': keyword,
            'per_page': per_page,
            'page': page
        }

        response = self.__session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        vacancies = response.json().get('items', [])

        return [
            {
                'name': vacancy['name'],
                'company': vacancy['employer']['name'],
                'url': vacancy['alternate_url'],
                'salary': vacancy['salary'],
                'id': vacancy['id']
            }
            for vacancy in vacancies
        ]


if __name__ == "__main__":
    hh_api = Hh_Api()
    vacancies = hh_api.get_vacancies('Python', 100, 2)

    try:
        for vacancy in vacancies:
            salary = vacancy['salary']
            if salary and salary['from'] is not None and salary['to'] is not None:
                avg_salary = salary['from'] + (salary['to'] - salary['from'] / 2)
            elif salary and salary['from'] is not None:
                avg_salary = salary['from']
            elif salary and salary['to'] is not None:
                avg_salary = salary['to']
            else:
                avg_salary = 0

            print(f"Название вакансии: {vacancy['name']}, "
                  f"Работадатель: {vacancy['company']}, "
                  f"Ссылка : {vacancy['url']}, "
                  f"Средняя зарплата: {vacancy['salary']}, "
                  f"id : {vacancy['id']}")
            print("="*270)

    except Exception as error:
        print(f"Произошла ошибка : {error}")
