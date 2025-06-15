# КУРСОВАЯ РАБОТА №2: Приложение для поиска вакансий на сайте HH.ru

## Данный проект является парсером по сайту HH.ru.
### 1. Класс API
### 2. Класс для работы с вакансиями
### 3. Клас для работы с json файлом
### 4. Функция взаимодействия с пользователем


# **Установка**:

### Для работы приложения необходимо установить интерпретатор *poetry*:

```pip install --user poetry```

### Так же клонируйте репозиторий:

```git clone https://github.com/Konstantin-Voronin-23/Project1.git```


# **Установка зависимостей**:

### Для работы проекта воспользуйтесь командами для установок зависимостей:

```
poetry add --group lint flake8
poetry add --group lint mypy
poetry add --group lint black
poetry add --group lint isort

poetry add --group dev pytest
poetry add --group dev pytest-cov
poetry add python-dotenv
poetry add requests
poetry add pandas
poetry add openpyxl
```


# **Реализация модулей**:

## 1. Модуль Utils - модуль для вспомогальных функций, в нем реализовано :

<details>
<summary><b>❗ ФУНКЦИИ ❗</b></summary>

### - Функция json_load :
    - Функция для чтения json файла

</details>

## 2. Модуль HH_API - это класс для реализация API сайта HH.ru по получению вакансий в нем реализованы:

<details>
<summary><b>❗ ФУНКЦИИ ❗</b></summary>

### - Метод init :
    - Метод инициализации класса
### - Метод url :
    - Метод получение приватного атрибута url
### - Метод headers :
    - Метод получение приватного атрибута headers
### - Метод vacancies :
    - Метод получение приватного атрибута vacancies
### - Метод response_check :
    - Проверяет доступность API - для внутренних методов
### - Метод get_vacancies :
    - Метод получает вакансии из API

</details>

## 3. Модуль Vacancy - это класс для реализация работы с вакансиями, в нем реализованы:

<details>
<summary><b>❗ ФУНКЦИИ ❗</b></summary>

### - Метод init :
    - Метод инициализации класса
### - Метод salary_from :
    - Валидация данных по зарплате для поля 'от'
### - Метод salary_to :
    - Валидация данных по зарплате для поля 'до'
### - Метод str :
    - Метод преобразования атрибутов в строку и вывод пользователю
### - Метод ge :
    - Проверяет, больше или равна средняя зарплата этой вакансии, чем у другой вакансии
### - Метод le :
    - Проверяет, меньше или равна средняя зарплата этой вакансии, чем у другой вакансии
### - Метод gt :
    - Проверяет, больше ли средняя зарплата этой вакансии, чем у другой вакансии
### - Метод lt :
    - Проверяет, меньше ли средняя зарплата этой вакансии, чем у другой вакансии
### - Метод cast_to_object_list :
    - Метод преобразует список JSON-объектов в список объектов Vacancy
### - Метод sort_vacancies_by_salary :
    - Метод сортировки списка вакансий по зарплате (по возрастанию или убыванию)
### - Метод to_dict :
    - Метод преобразует объект Vacancy в словарь для сериализации в JSON
### - Метод load_from_json :
    - Метод Загружает список вакансий из JSON-файла обратно в объекты Vacancy

</details>

## 4. Модуль File_Handler - это класс для реализация работы с файлами, в нем реализованы:

<details>
<summary><b>❗ ФУНКЦИИ ❗</b></summary>

### - Метод init :
    - Метод инициализации класса
### - Метод filepath :
    - Метод получение приватного атрибута filepath
### - Метод write_to_file :
    - Защищеный метод записи в файл
### - Метод save_to_json :
    - Метод сохранения данных в json
### - Метод load_from_json :
    - Метод загрузки данных в json
### - Метод clear_file :
    - Метод полной чистки файла
### - Метод add_vacancy :
    - Метод добавления вакансий в файл
### - Метод delete_vacancy_by_id :
    - Метод удаления вакансии по ID
### - Метод search_vacancies_by_keyword :
    - Метод поиска вакансии по ключевому слову во всех полях: name, description, area.
### - Метод filter_vacancies_by_keyword :
    - Метод фильтрации вакансий по критериям
### - Метод filter_vacancies_by_salary_range :
    - Метод фильтрации по диапозону ЗП
### - Метод load_vacancies :
    - Метод загружает вакансии и возвращает их как объекты Vacancy

</details>

# **Тестирование модулей**:

## 1. Модуль Utils

<details>
<summary><b>❗ МОДУЛЬ UTILS ❗</b></summary>

### - test_load_valid_json
    - Тест загрузки корректного JSON файла
### - test_load_nonexistent_file
    - Тест загрузки несуществующего файла
### - test_load_invalid_json
    - Тест загрузки некорректного JSON
### - test_load_empty_file
    - Тест загрузки пустого файла
### - test_load_not_list_json
    - Тест загрузки JSON, который не является списком

</details>

## 2. Модуль HH_API

<details>
<summary><b>❗ МОДУЛЬ HH_API ❗</b></summary>

### - test_url_property_valid
    - Проверяем, что url возвращает правильное значение
### - test_headers_property_valid
    - Проверяем, что headers содержит User-Agent
### - test_vacancies_property_valid
    - Проверяем, что vacancies возвращает список
### - test_response_check_success
    - Проверяем успешную проверку ответа API
### - test_response_check_failure
    - Проверяем неудачную проверку ответа API
### - test_get_vacancies_success
    - Проверяем успешное получение вакансий
### - test_get_vacancies_api_unavailable
    - Проверяем обработку недоступного API
### - test_get_vacancies_request_error
    - Проверяем обработку ошибки запроса
### - test_url_property
    - Тест для свойства url
### - test_headers_property
    - Тест для свойства headers
### - test_vacancies_property
    - Тест для свойства vacancies

</details>

## 3. Модуль Vacancy

<details>
<summary><b>❗ МОДУЛЬ Vacancy ❗</b></summary>

### - test_vacancy_creation
    - Тест создания вакансии с полными данными
### - test_vacancy_with_minimal_data
    - Тест создания вакансии с минимальными данными
### - test_str_representation
    - Тест строкового представления вакансии
### - test_comparison_operators
    - Тест операторов сравнения
### - test_to_dict_method
    - Тест преобразования вакансии в словарь
### - test_cast_to_object_list
    - Тест преобразования списка словарей в список вакансий
### - test_sort_vacancies_by_salary
    - Тест сортировки вакансий по зарплате
### - test_salary_from_validation
    - Тест валидации поля salary_from
### - test_salary_to_validation
    - Тест валидации поля salary_to
### - test_str_representation_1
    - Тест строкового представления вакансии
### - test_comparison_operators_1
    - Тест операторов сравнения
### - test_cast_to_object_list_1
    - Тест преобразования JSON в список объектов
### - test_dict_conversion_and_json_io
    - Тест преобразования в словарь и работы с JSON

</details>

## 4. Модуль File_Handler

<details>
<summary><b>❗ МОДУЛЬ File_Handler ❗</b></summary>

### - test_filepath_property
    - Тест свойства filepath
### - test_save_and_load_empty_json
    - ест сохранения и загрузки пустого JSON
### - test_save_and_load_vacancies
    - Тест сохранения и загрузки вакансий
### - test_add_vacancy
    - Тест добавления вакансии
### - test_add_duplicate_vacancy
    - Тест добавления дубликата вакансии
### - test_delete_vacancy_by_id
    - Тест удаления вакансии по ID
### - test_search_vacancies_by_keyword
    - Тест поиска вакансий по ключевому слову
### - test_filter_vacancies_by_keyword
    - Тест фильтрации вакансий по ключевому слову
### - test_filter_vacancies_by_salary_range
    - Тест фильтрации вакансий по диапазону зарплат
### - test_clear_file
    - Тест очистки файла
### - test_load_vacancies_as_objects
    - Тест загрузки вакансий как объектов Vacancy
### - test_write_to_file_success
    - Тест успешной записи в файл
### - test_write_to_file_error
    - Тест ошибки записи в файл
### - test_save_to_json_with_vacancy_objects
    - Тест сохранения с объектом
### - test_save_to_json_with_dicts
    - Тест сохранения с словарем
### - test_add_vacancy_new
    - Тест добавления новой вакансии
### - test_add_vacancy_duplicate
    - Тест добавления дубликата вакансии
### - test_delete_vacancy_by_id_exists
    - Тест успешного удаления вакансии
### - test_delete_vacancy_by_id_not_exists
    - Тест удаления не существующей вакансии
### - test_search_vacancies_by_keyword
    - Тест поиска вакансии по слову
### - test_filter_vacancies_by_keyword
    - Тест фильтрации вакансий по слову
### - test_filter_vacancies_by_salary_range
    - Тест фильтрации вакансии по зарплате
### - test_filter_vacancies_by_salary_range_invalid_format
    - Тест фильтрации зарплаты в невалидном формате
### - test_load_vacancies
    - Тест валидной загрузки вакансий
### - test_clear_file
    - Тест очистки файла

</details>

# Покрытие тестами 87%

# Документация

# Лицензия

## - Этот проект лицензирован по [лицензии MIT](LICENSE).