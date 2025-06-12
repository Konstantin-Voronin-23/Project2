import json
import os
import re
from typing import Union
from src.Vacancy import Vacancy
from abc import ABC, abstractmethod


class BaseFile(ABC):
    """Абстрактный класс для работы с файлами и данными"""

    @property
    @abstractmethod
    def filepath(self):
        """Метод получение приватного атрибута filepath"""
        pass

    @abstractmethod
    def save_to_json(self, vacancies):
        """Абстрактный метод загрузки сохранения в json"""
        pass

    @abstractmethod
    def load_from_json(self):
        """Абстрактный метод загрузки данных из json"""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Абстрактный метод добавления вакансий"""
        pass

    @abstractmethod
    def delete_vacancy_by_id(self, id):
        """Абстрактный метод удаления вакансий по критерию"""
        pass

    @abstractmethod
    def search_vacancies_by_keyword(self, keyword):
        """Абстрактный метод поиска вакансии по ключевому слову"""
        pass

    @abstractmethod
    def filter_vacancies_by_keyword(self, keyword):
        """Абстрактный Метод фильтрации вакансии по ключевому слову"""
        pass

    @abstractmethod
    def filter_vacancies_by_salary_range(self, salary_range):
        """Абстрактный Метод фильтрации вакансии по диапазону зарплат"""
        pass


class FileHandlerJson(BaseFile):
    """Класс для сохранения и загрузки данных о вакансиях в/из JSON-файла."""

    def __init__(self):
        """Метод инициализации класса"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__filepath = os.path.join(script_dir, "../data/vacancies_hh.json")
        os.makedirs(os.path.dirname(self.__filepath), exist_ok=True)

    @property
    def filepath(self):
        """Метод получение приватного атрибута filepath"""
        return self.__filepath

    def _write_to_file(self, data: list) -> None:
        """Защищеный метод записи в файл"""
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("Данные успешно записаны в файл.")
        except Exception as e:
            raise IOError(f"Ошибка при записи в файл: {e}")

    def save_to_json(self, vacancies: list) -> None:
        """Метод сохранения данных в json"""
        try:
            if isinstance(vacancies[0], Vacancy):
                data = [vacancy.to_dict() for vacancy in vacancies]
            else:
                data = vacancies
            print("Пример данных для записи:", data[:2])
            self._write_to_file(data)
            print(f"Данные успешно сохранены в {self.filepath}")
        except Exception as e:
            print(f"Ошибка при сохранении данных в JSON: {e}")

    def load_from_json(self) -> list:
        """Метод загрузки данных в json"""
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Файл {self.filepath} не найден.")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON из файла {self.filepath}.")
            return []

    def clear_file(self) -> None:
        """Метод полной чистки файла"""
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                file.write("[]")
            print(f"Файл {self.filepath} очищен.")
        except Exception as e:
            print(f"Ошибка при очистке файла: {e}")

    def add_vacancy(self, vacancy: Union[Vacancy, dict]) -> None:
        """Метод добавления вакансий в файл"""
        current_data = self.load_from_json()

        if isinstance(vacancy, Vacancy):
            vacancy_dict = vacancy.to_dict()
        elif isinstance(vacancy, dict):
            vacancy_dict = vacancy
        else:
            raise ValueError("Можно добавлять только объект Vacancy или словарь.")

        existing_id = {item["id"] for item in current_data}
        if vacancy_dict["id"] in existing_id:
            print("Вакансия с такой ссылкой уже существует. Дубликат не добавлен.")
            return

        current_data.append(vacancy_dict)

        try:
            self._write_to_file(current_data)
            print("Новая вакансия успешно добавлена.")
        except IOError as e:
            print(e)

    def delete_vacancy_by_id(self, id: str) -> None:
        """Метод удаления вакансии по ID"""
        data = self.load_from_json()
        filtered_data = [item for item in data if item.get("id") != id]

        if len(data) == len(filtered_data):
            print(f"Вакансия с ссылкой {id} не найдена.")
        else:
            self._write_to_file(filtered_data)
            print(f"Вакансия с ссылкой {id} успешно удалена.")

    def search_vacancies_by_keyword(self, keyword: str) -> list:
        """
        Метод поиска вакансии по ключевому слову во всех полях: name, description, area.
        """
        data = self.load_from_json()
        pattern = re.compile(keyword, re.IGNORECASE)

        result = [
            item
            for item in data
            if pattern.search(item.get("name", ""))
            or pattern.search(item.get("description", ""))
            or pattern.search(item.get("area", ""))
        ]

        print(f"Найдено {len(result)} вакансий по ключевому слову '{keyword}'.")
        return result

    def filter_vacancies_by_keyword(self, keyword: str) -> list[Vacancy]:
        """Метод фильтрации вакансий по критериям"""
        data = self.load_from_json()
        pattern = re.compile(keyword, re.IGNORECASE)

        filtered_data = [
            item
            for item in data
            if pattern.search(item.get("name", ""))
            or pattern.search(item.get("description", ""))
            or pattern.search(item.get("area", ""))
        ]

        result = Vacancy.cast_to_object_list(filtered_data)
        print(f"Отфильтровано {len(result)} вакансий по ключевому слову '{keyword}'.")
        return result

    def filter_vacancies_by_salary_range(self, salary_range: str) -> list[Vacancy]:
        """Метод фильтрации по диапозону ЗП"""
        try:
            min_salary, max_salary = map(int, salary_range.split("-"))
        except ValueError:
            raise ValueError("Диапазон зарплат должен быть в формате 'мин-макс', например '50000-100000'.")

        data = self.load_from_json()
        filtered_data = []

        for item in data:
            salary_from = item.get("salary_from", 0)
            salary_to = item.get("salary_to", 0)

            if (salary_from and min_salary <= salary_from <= max_salary) or (
                salary_to and min_salary <= salary_to <= max_salary
            ):
                filtered_data.append(item)

        result = Vacancy.cast_to_object_list(filtered_data)
        print(f"Отфильтровано {len(result)} вакансий по диапазону зарплат {salary_range}.")
        return result

    def load_vacancies(self) -> list[Vacancy]:
        """Метод загружает вакансии и возвращает их как объекты Vacancy"""
        data = self.load_from_json()
        return Vacancy.cast_to_object_list(data)
