from abc import ABC, abstractmethod
import requests
from config import USER_AGENT
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_json = os.path.join(script_dir, "../data/vacancy_hh.json")


class BaseApi(ABC):
    """Базовый абстрактный класс для подключения к API"""

    @property
    @abstractmethod
    def url(self) -> str:
        """Метод получение приватного атрибута url"""
        pass

    @property
    @abstractmethod
    def headers(self) -> dict:
        """Метод получение приватного атрибута headers"""
        pass

    @abstractmethod
    def get_vacancies(self, text) -> list:
        """Метод получение приватного атрибута vacancies"""
        pass


class HeadHunterAPI(BaseApi):
    """Метод запроса через API"""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": USER_AGENT}
        self.__vacancies = []

    @property
    def url(self) -> str:
        """Метод получение приватного атрибута url"""
        return self.__url

    @property
    def headers(self) -> dict:
        """Метод получение приватного атрибута headers"""
        return self.__headers

    @property
    def vacancies(self) -> list:
        """Метод получение приватного атрибута vacancies"""
        return self.__vacancies

    def __response_check(self) -> bool:
        """Проверяет доступность API - для внутренних методов"""
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()  # if status_code == 200
            return True
        except requests.exceptions.RequestException:
            return False

    def get_vacancies(self, text: str, per_page: int = 10) -> list[dict]:
        """Получает вакансии из API"""
        if not self.__response_check():
            raise ConnectionError("API недоступно. Невозможно получить вакансии.")

        params = {"text": text, "per_page": per_page}
        try:
            response = requests.get(self.url, headers=self.headers, params=params)
            response.raise_for_status()
            self.__vacancies = response.json().get("items", [])
            return self.__vacancies
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Ошибка при выполнении запроса: {e}") from e
