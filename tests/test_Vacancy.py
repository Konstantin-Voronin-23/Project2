import unittest

from src.Vacancy import Vacancy


class TestVacancy_one(unittest.TestCase):
    """Класс для проверки модуля Vacancy"""
    def setUp(self):
        """Подготовка тестовых данных"""
        self.sample_data = {
            "name": "Python Developer",
            "id": "12345",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "area": {"name": "Москва"},
            "description": "Разработка на Python",
        }

        self.minimal_data = {
            "name": "Junior Developer",
            "id": "67890",
            "salary": None,
            "area": None,
            "description": None,
        }

    def test_vacancy_creation(self):
        """Тест создания вакансии с полными данными"""
        vacancy = Vacancy(**self.sample_data)

        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.id, "12345")
        self.assertEqual(vacancy.area, "Москва")
        self.assertEqual(vacancy.description, "Разработка на Python")
        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)

    def test_vacancy_with_minimal_data(self):
        """Тест создания вакансии с минимальными данными"""
        vacancy = Vacancy(**self.minimal_data)

        self.assertEqual(vacancy.name, "Junior Developer")
        self.assertEqual(vacancy.id, "67890")
        self.assertEqual(vacancy.area, "Не указано")
        self.assertEqual(vacancy.description, "")
        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 0)

    def test_str_representation(self):
        """Тест строкового представления вакансии"""
        vacancy = Vacancy(**self.sample_data)
        str_repr = str(vacancy)

        self.assertIn("Python Developer", str_repr)
        self.assertIn("https://hh.ru/vacancy/12345", str_repr)
        self.assertIn("Москва", str_repr)
        self.assertIn("100000", str_repr)
        self.assertIn("150000", str_repr)

    def test_comparison_operators(self):
        """Тест операторов сравнения"""

        high_vacancy = Vacancy(
            name="Senior",
            id="1",
            salary={"from": 200000, "to": 250000},
            area="Москва",
            description="Senior position"
        )

        mid_vacancy = Vacancy(**self.sample_data)

        low_vacancy = Vacancy(
            name="Junior",
            id="2",
            salary={"from": 50000, "to": 70000},
            area="Москва",
            description="Junior position"
        )

        self.assertTrue(high_vacancy > mid_vacancy)
        self.assertTrue(low_vacancy < mid_vacancy)
        self.assertTrue(mid_vacancy >= Vacancy(**self.sample_data))
        self.assertTrue(mid_vacancy <= Vacancy(**self.sample_data))

    def test_to_dict_method(self):
        """Тест преобразования вакансии в словарь"""
        vacancy = Vacancy(**self.sample_data)
        vacancy_dict = vacancy.to_dict()

        self.assertEqual(vacancy_dict["name"], "Python Developer")
        self.assertEqual(vacancy_dict["id"], "12345")
        self.assertEqual(vacancy_dict["area"], "Москва")
        self.assertEqual(vacancy_dict["description"], "Разработка на Python")
        self.assertEqual(vacancy_dict["salary_from"], 100000)
        self.assertEqual(vacancy_dict["salary_to"], 150000)
        self.assertIn("currency", vacancy_dict["salary"])

    def test_cast_to_object_list(self):
        """Тест преобразования списка словарей в список вакансий"""
        test_data = [self.sample_data, self.minimal_data]
        vacancies = Vacancy.cast_to_object_list(test_data)

        self.assertEqual(len(vacancies), 2)
        self.assertIsInstance(vacancies[0], Vacancy)
        self.assertIsInstance(vacancies[1], Vacancy)
        self.assertEqual(vacancies[0].name, "Python Developer")
        self.assertEqual(vacancies[1].name, "Junior Developer")

    def test_sort_vacancies_by_salary(self):
        """Тест сортировки вакансий по зарплате"""

        high_vacancy = Vacancy(
            name="Senior",
            id="1",
            salary={"from": 200000},
            area="Москва",
            description="Senior"
        )

        mid_vacancy = Vacancy(**self.sample_data)

        low_vacancy = Vacancy(
            name="Junior",
            id="2",
            salary={"from": 50000},
            area="Москва",
            description="Junior"
        )

        vacancies = [low_vacancy, mid_vacancy, high_vacancy]

        sorted_asc = Vacancy.sort_vacancies_by_salary(vacancies, reverse=False)
        self.assertEqual(sorted_asc[0].salary_from, 50000)
        self.assertEqual(sorted_asc[1].salary_from, 100000)
        self.assertEqual(sorted_asc[2].salary_from, 200000)

        sorted_desc = Vacancy.sort_vacancies_by_salary(vacancies, reverse=True)
        self.assertEqual(sorted_desc[0].salary_from, 200000)
        self.assertEqual(sorted_desc[1].salary_from, 100000)
        self.assertEqual(sorted_desc[2].salary_from, 50000)

    def test_salary_from_validation(self):
        """Тест валидации поля salary_from"""

        vacancy = Vacancy("Test", "1", {"from": "1000"}, "Moscow", "Test")
        self.assertEqual(vacancy.salary_from, 1000)

        vacancy = Vacancy("Test", "1", {"from": None}, "Moscow", "Test")
        self.assertEqual(vacancy.salary_from, 0)

    def test_salary_to_validation(self):
        """Тест валидации поля salary_to"""

        vacancy = Vacancy("Test", "1", {"to": "2000"}, "Moscow", "Test")
        self.assertEqual(vacancy.salary_to, 2000)

        vacancy = Vacancy("Test", "1", {"to": None}, "Moscow", "Test")
        self.assertEqual(vacancy.salary_to, 0)

    def test_str_representation_1(self):
        """Тест строкового представления вакансии"""

        vacancy = Vacancy("Developer", "123", {"from": 1000, "to": 2000}, "Moscow", "Backend")
        self.assertIn("Вакансия: Developer", str(vacancy))
        self.assertIn("Зарплата от: 1000", str(vacancy))

    def test_comparison_operators_1(self):
        """Тест операторов сравнения"""

        v1 = Vacancy("A", "1", {"from": 1000}, "M", "D")
        v2 = Vacancy("B", "2", {"from": 2000}, "M", "D")

        self.assertTrue(v1 < v2)
        self.assertTrue(v2 > v1)
        self.assertTrue(v1 <= v2)
        self.assertTrue(v2 >= v1)

    def test_cast_to_object_list_1(self):
        """Тест преобразования JSON в список объектов"""

        test_data = [{
            "name": "Test",
            "id": "1",
            "area": {"name": "Moscow"},
            "snippet": {"responsibility": "Test desc"},
            "salary": {"from": 1000}
        }]
        vacancies = Vacancy.cast_to_object_list(test_data)
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].name, "Test")

    def test_dict_conversion_and_json_io(self):
        """Тест преобразования в словарь и работы с JSON"""

        vacancy = Vacancy("Test", "1", {"from": 1000}, "Moscow", "Desc")
        vacancy_dict = vacancy.to_dict()

        self.assertEqual(vacancy_dict["name"], "Test")
        self.assertEqual(vacancy_dict["salary_from"], 1000)

        loaded = Vacancy.load_from_json("nonexistent.json")
        self.assertEqual(loaded, [])
