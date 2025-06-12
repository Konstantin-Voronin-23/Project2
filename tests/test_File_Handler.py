import os
import pytest
import unittest
import tempfile
import shutil
import json
from src.Vacancy import Vacancy
from src.File_Handler import FileHandlerJson


class TestFileHandlerJson(unittest.TestCase):
    """Класс для проверки модуля File_Handler"""

    def setUp(self):
        """Создание временной директории и файла для тестов"""

        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_vacancies.json")
        self.handler = FileHandlerJson()
        self.handler._FileHandlerJson__filepath = self.test_file

        self.sample_vacancy = {
            "id": "1",
            "name": "Python Developer",
            "description": "Разработчик Python",
            "area": "Москва",
            "salary_from": 100000,
            "salary_to": 150000
        }
        self.sample_vacancy2 = {
            "id": "2",
            "name": "Java Developer",
            "description": "Разработчик Java",
            "area": "Санкт-Петербург",
            "salary_from": 90000,
            "salary_to": 120000
        }

    def tearDown(self):
        """Удаление временной директории после тестов"""

        shutil.rmtree(self.test_dir)

    def test_filepath_property(self):
        """Тест свойства filepath"""

        self.assertEqual(self.handler.filepath, self.test_file)

    def test_save_and_load_empty_json(self):
        """Тест сохранения и загрузки пустого JSON"""

        self.handler.save_to_json([])
        loaded_data = self.handler.load_from_json()
        self.assertEqual(loaded_data, [])

    def test_save_and_load_vacancies(self):
        """Тест сохранения и загрузки вакансий"""

        self.handler.save_to_json([self.sample_vacancy])

        loaded_data = self.handler.load_from_json()
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]["name"], "Python Developer")

    def test_add_vacancy(self):
        """Тест добавления вакансии"""

        self.handler.add_vacancy(self.sample_vacancy)
        loaded_data = self.handler.load_from_json()
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]["id"], "1")

    def test_add_duplicate_vacancy(self):
        """Тест добавления дубликата вакансии"""

        self.handler.add_vacancy(self.sample_vacancy)
        self.handler.add_vacancy(self.sample_vacancy)
        loaded_data = self.handler.load_from_json()
        self.assertEqual(len(loaded_data), 1)

    def test_delete_vacancy_by_id(self):
        """Тест удаления вакансии по ID"""

        self.handler.add_vacancy(self.sample_vacancy)
        self.handler.add_vacancy(self.sample_vacancy2)

        self.handler.delete_vacancy_by_id("1")
        loaded_data = self.handler.load_from_json()
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]["id"], "2")

    def test_search_vacancies_by_keyword(self):
        """Тест поиска вакансий по ключевому слову"""

        self.handler.add_vacancy(self.sample_vacancy)
        self.handler.add_vacancy(self.sample_vacancy2)

        results = self.handler.search_vacancies_by_keyword("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Python Developer")

    def test_filter_vacancies_by_keyword(self):
        """Тест фильтрации вакансий по ключевому слову"""

        self.handler.add_vacancy(self.sample_vacancy)
        self.handler.add_vacancy(self.sample_vacancy2)

        results = self.handler.filter_vacancies_by_keyword("Java")
        self.assertEqual(len(results), 1)
        self.assertTrue(isinstance(results[0], Vacancy))
        self.assertEqual(results[0].name, "Java Developer")

    def test_filter_vacancies_by_salary_range(self):
        """Тест фильтрации вакансий по диапазону зарплат"""

        self.handler.add_vacancy(self.sample_vacancy)
        self.handler.add_vacancy(self.sample_vacancy2)

        results = self.handler.filter_vacancies_by_salary_range("80000-110000")
        self.assertEqual(len(results), 2)

        narrow_results = self.handler.filter_vacancies_by_salary_range("95000-105000")
        self.assertEqual(len(narrow_results), 1)
        self.assertEqual(narrow_results[0].name, "Python Developer")

    def test_clear_file(self):
        """Тест очистки файла"""

        self.handler.add_vacancy(self.sample_vacancy)
        self.handler.clear_file()
        loaded_data = self.handler.load_from_json()
        self.assertEqual(loaded_data, [])

    def test_load_vacancies_as_objects(self):
        """Тест загрузки вакансий как объектов Vacancy"""

        self.handler.add_vacancy(self.sample_vacancy)
        vacancies = self.handler.load_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertTrue(isinstance(vacancies[0], Vacancy))
        self.assertEqual(vacancies[0].name, "Python Developer")


def test_write_to_file_success(tmp_path):
    """Тест успешной записи в файл"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    test_data = [{"id": "1", "name": "Test Vacancy"}]

    file_handler._write_to_file(test_data)

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert data == test_data


def test_write_to_file_error():
    """Тест ошибки записи в файл"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = "/invalid/path/test_vacancies.json"

    with pytest.raises(IOError):
        file_handler._write_to_file([{"id": "1"}])


def test_save_to_json_with_vacancy_objects(tmp_path):
    """Тест сохранения с объектом"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancy = Vacancy(
        id="1",
        name="Test",
        salary={"from": 1000, "to": 2000},
        description="Test description",
        area = "Test area"
    )

    file_handler.save_to_json([vacancy])

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1
    assert data[0]["id"] == "1"


def test_save_to_json_with_dicts(tmp_path):
    """Тест сохранения с словарем"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancies = [{"id": "1", "name": "Test"}]
    file_handler.save_to_json(vacancies)

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert data == vacancies


def test_add_vacancy_new(tmp_path):
    """Тест добавления новой вакансии"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancy = Vacancy(
        id="1",
        name="Test",
        salary={"from": 1000, "to": 2000},
        description="Test description",
        area="Test area"
    )
    file_handler.add_vacancy(vacancy)

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1
    assert data[0]["id"] == "1"


def test_add_vacancy_duplicate(tmp_path):
    """Тест добавления дубликата вакансии"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancy = Vacancy(
        id="1",
        name="Test",
        salary={"from": 1000, "to": 2000},
        description="Test description",
        area="Test area"
    )
    file_handler.add_vacancy(vacancy)
    file_handler.add_vacancy(vacancy)

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1


def test_delete_vacancy_by_id_exists(tmp_path):
    """Тест успешного удаления вакансии"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancy = {"id": "1", "name": "Test"}
    with open(file_handler.filepath, "w", encoding="utf-8") as file:
        json.dump([vacancy], file)

    file_handler.delete_vacancy_by_id("1")

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 0


def test_delete_vacancy_by_id_not_exists(tmp_path):
    """Тест удаления не существующей вакансии"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancy = {"id": "1", "name": "Test"}
    with open(file_handler.filepath, "w", encoding="utf-8") as file:
        json.dump([vacancy], file)

    file_handler.delete_vacancy_by_id("2")

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1


def test_search_vacancies_by_keyword(tmp_path):
    """Тест поиска вакансии по слову"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancies = [
        {"id": "1", "name": "Python Developer", "description": "Need Python skills", "area": "Moscow"},
        {"id": "2", "name": "Java Developer", "description": "Need Java skills", "area": "London"}
    ]
    with open(file_handler.filepath, "w", encoding="utf-8") as file:
        json.dump(vacancies, file)

    result = file_handler.search_vacancies_by_keyword("Python")
    assert len(result) == 1
    assert result[0]["id"] == "1"


def test_filter_vacancies_by_keyword(tmp_path):
    """Тест фильтрации вакансий по слову"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancies = [
        {"id": "1", "name": "Python Developer", "description": "Need Python skills", "area": "Moscow"},
        {"id": "2", "name": "Java Developer", "description": "Need Java skills", "area": "London"}
    ]
    with open(file_handler.filepath, "w", encoding="utf-8") as file:
        json.dump(vacancies, file)

    result = file_handler.filter_vacancies_by_keyword("Python")
    assert len(result) == 1
    assert isinstance(result[0], Vacancy)
    assert result[0].id == "1"


def test_filter_vacancies_by_salary_range(tmp_path):
    """Тест фильтрации вакансии по зарплате"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancies = [
        {"id": "1", "name": "Python", "salary_from": 50000, "salary_to": 70000},
        {"id": "2", "name": "Java", "salary_from": 80000, "salary_to": 100000}
    ]
    with open(file_handler.filepath, "w", encoding="utf-8") as file:
        json.dump(vacancies, file)

    result = file_handler.filter_vacancies_by_salary_range("60000-90000")
    assert len(result) == 2
    assert isinstance(result[0], Vacancy)


def test_filter_vacancies_by_salary_range_invalid_format():
    """Тест фильтрации зарплаты в невалидном формате"""

    file_handler = FileHandlerJson()
    with pytest.raises(ValueError):
        file_handler.filter_vacancies_by_salary_range("invalid-format")


def test_load_vacancies(tmp_path):
    """Тест валидной загрузки вакансий"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    vacancies = [{"id": "1", "name": "Python"}]
    with open(file_handler.filepath, "w", encoding="utf-8") as file:
        json.dump(vacancies, file)

    result = file_handler.load_vacancies()
    assert len(result) == 1
    assert isinstance(result[0], Vacancy)
    assert result[0].id == "1"


def test_clear_file(tmp_path):
    """Тест очистки файла"""

    file_handler = FileHandlerJson()
    file_handler._FileHandlerJson__filepath = tmp_path / "test_vacancies.json"
    with open(file_handler.filepath, "w", encoding="utf-8") as file:
        json.dump([{"id": "1"}], file)

    file_handler.clear_file()

    with open(file_handler.filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert data == []
