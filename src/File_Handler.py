import json
from abc import abstractmethod, ABC
import os


class FileHandler(ABC):
    """Класс для работы с файлами"""

    def __init__(self, filename):
        """Метод инициализации"""
        self.__filename = filename

    @abstractmethod
    def get_vacancies(self, **criteria):
        """Получение вакансий из json файла"""
        pass


class FileHandlerJson(FileHandler):
    """Класс для работы с json файлом"""

    def __init__(self, filename='./data/vacancies.json'):
        super().__init__(filename)
        self._filename = filename

    def get_vacancies(self, **criteria):
        """Получение вакансий из json файла с фильтрацией по критериям."""
        if not os.path.exists(self._FileHandler__filename):
            return []

        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

        vacancies = data.get('items', data) if isinstance(data, dict) else data

        if not isinstance(vacancies, list):
            return []

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            if not isinstance(vacancy, dict):
                continue

            match = True
            for key, value in criteria.items():
                if vacancy.get(key) != value:
                    match = False
                    break

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def add_vacancy(self, vacancy):
        """Добавление вакансии в json файл"""

        vacancies = self.get_vacancies()
        if not any(v == vacancy for v in vacancies):
            vacancies.append(vacancy)
            self.save_vacancies(vacancies)
            return True
        return False

    def delete_vacancy(self, vacancy):
        """Удаление вакансий из json файла"""

        vacancies = self.get_vacancies()

        initial_length = len(vacancies)
        vacancies = [v for v in vacancies if v != vacancy]

        if len(vacancies) < initial_length:
            self.save_vacancies(vacancies)
            return True
        return False
