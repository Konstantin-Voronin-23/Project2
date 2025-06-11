class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ('_title', '_url', '_salary', '_description', '_requirements')

    def __init__(self, title: str, url: str, salary: dict | None, description: str, requirements: str):
        """Метод инициализации"""

        self._title = title
        self._url = url
        self._salary = self._validate_salary(salary)
        self._description = description
        self._requirements = requirements

    def _validate_salary(self, salary: dict | None) -> dict:
        """Приватный метод для валидации зарплаты."""
        if not salary:
            return {"from": 0, "to": 0, "currency": "не указана"}

        validated = {
            "from": salary.get("from", 0),
            "to": salary.get("to", 0),
            "currency": salary.get("currency", "не указана").lower()
        }

        if validated["from"] == 0 and validated["to"] == 0:
            validated["currency"] = "не указана"

        return validated

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary(self) -> dict:
        return self._salary

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    def __str__(self) -> str:
        """Метод вывода данных пользователю"""
        salary_from = f"от {self._salary['from']}" if self._salary['from'] else ""
        salary_to = f"до {self._salary['to']}" if self._salary['to'] else ""
        salary_currency = self._salary['currency']

        salary_str = " ".join(filter(None, [salary_from, salary_to, salary_currency]))
        if not salary_str:
            salary_str = "Зарплата не указана"

        return (f"Вакансия: {self._title}\n"
                f"Ссылка: {self._url}\n"
                f"Зарплата: {salary_str}\n"
                f"Описание: {self._description}\n"
                f"Требования: {self._requirements}")

    def __repr__(self) -> str:
        """Метод вывода данных в консоль"""
        return f"Vacancy(title={self._title!r}, url={self._url!r}, salary={self._salary!r})"

    def __eq__(self, other) -> bool:
        """Проверяет, равна ли средняя зарплата этой вакансии средней зарплате другой вакансии."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other) -> bool:
        """Проверяет, меньше ли средняя зарплата этой вакансии, чем у другой вакансии."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other) -> bool:
        """Проверяет, меньше или равна средняя зарплата этой вакансии, чем у другой вакансии."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other) -> bool:
        """Проверяет, больше ли средняя зарплата этой вакансии, чем у другой вакансии."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other) -> bool:
        """Проверяет, больше или равна средняя зарплата этой вакансии, чем у другой вакансии."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary

    @property
    def avg_salary(self) -> float:
        """Среднее значение зарплаты для сравнения вакансий."""
        if self._salary["from"] and self._salary["to"]:
            return (self._salary["from"] + self._salary["to"]) / 2
        elif self._salary["from"]:
            return self._salary["from"]
        elif self._salary["to"]:
            return self._salary["to"]
        return 0
