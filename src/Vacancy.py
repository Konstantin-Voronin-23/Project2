import json
from typing import Any, Dict, List, Union

from src.utils import json_load


class Vacancy:
    """Класс для обработки вакансий"""

    __slots__ = (
        "name",
        "id",
        "area",
        "__salary",
        "description",
        "salary_from",
        "salary_to",
    )

    def __init__(self, name: str, id: str, salary: dict[str, Union[int, float]], area: str, description: str) -> None:
        """Метод инициализации класса"""

        self.name = name
        self.id = id

        if isinstance(area, dict):
            self.area = area.get("name", "Не указано")
        else:
            self.area = area or "Не указано"

        self.__salary = salary or {}
        self.description = description or ""
        self.salary_from = self.__salary_from()
        self.salary_to = self.__salary_to()

    def __salary_from(self) -> int:
        """Валидация данных по зарплате для поля 'от'"""
        self.salary_from = 0
        if self.__salary:
            self.salary_from = self.__salary.get("from") or 0

            try:
                self.salary_from = int(self.salary_from)
            except (TypeError, ValueError):
                self.salary_from = 0
        return self.salary_from

    def __salary_to(self) -> int:
        """Валидация данных по зарплате для поля 'до'"""
        self.salary_to = 0
        if self.__salary:  #
            self.salary_to = self.__salary.get("to") or 0

            try:
                self.salary_to = int(self.salary_to)
            except (TypeError, ValueError):
                self.salary_to = 0
        return self.salary_to

    def __str__(self) -> str:
        """Метод преобразования атрибутов в строку и вывод пользователю"""

        hh_link = f"https://hh.ru/vacancy/{self.id}"

        return (
            f"Вакансия: {self.name}\n"
            f"Ссылка: {hh_link}\n"
            f"Расположение: {self.area}\n"
            f"Описание: {self.description}\n"
            f"Зарплата от: {self.salary_from}\n"
            f"Зарплата до: {self.salary_to}\n"
            "--------------------------"
        )

    def __ge__(self, other: Any) -> bool:
        """Проверяет, больше или равна средняя зарплата этой вакансии, чем у другой вакансии."""
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from >= other.salary_from

    def __le__(self, other: Any) -> bool:
        """Проверяет, меньше или равна средняя зарплата этой вакансии, чем у другой вакансии."""
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from <= other.salary_from

    def __gt__(self, other: Any) -> bool:
        """Проверяет, больше ли средняя зарплата этой вакансии, чем у другой вакансии."""
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from > other.salary_from

    def __lt__(self, other: Any) -> bool:
        """Проверяет, меньше ли средняя зарплата этой вакансии, чем у другой вакансии"""
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from < other.salary_from

    @staticmethod
    def cast_to_object_list(data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Метод преобразует список JSON-объектов в список объектов Vacancy."""
        vacancy_list = []

        for item in data:
            try:
                name = item.get("name")
                id = item.get("id")

                area = item.get("area", {})

                snippet = item.get("snippet", {})
                responsibility = snippet.get("responsibility")
                description = responsibility or item.get("description", "")

                salary = item.get("salary", {})

                vacancy = Vacancy(name=name, id=id, area=area, salary=salary, description=description)
                vacancy_list.append(vacancy)

            except Exception as e:
                print(f"Ошибка при обработке вакансии: {e}")
                continue

        return vacancy_list

    @staticmethod
    def sort_vacancies_by_salary(vacancies: list["Vacancy"], reverse: bool = True) -> list["Vacancy"]:
        """Метод сортировки списка вакансий по зарплате (по возрастанию или убыванию)"""
        return sorted(vacancies, key=lambda v: v.salary_from, reverse=reverse)

    def to_dict(self) -> dict:
        """Метод преобразует объект Vacancy в словарь для сериализации в JSON"""
        return {
            "name": self.name,
            "id": self.id,
            "area": self.area,
            "salary": self.__salary,  # Сохраняем оригинальный словарь с зарплатой
            "description": self.description,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
        }

    @staticmethod
    def load_from_json(filename: str) -> List["Vacancy"]:
        """Метод Загружает список вакансий из JSON-файла обратно в объекты Vacancy"""
        try:
            data = json_load(filename)

            vacancies = []
            for item in data:
                vacancy = Vacancy(
                    name=item["name"],
                    id=item["id"],
                    area=item["area"],
                    salary=item["salary"],
                    description=item["description"],
                )
                vacancies.append(vacancy)
            return vacancies

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка при чтении JSON из файла {filename}.")
            return []
