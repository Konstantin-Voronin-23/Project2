from src.HH_API import HeadHunterAPI
from src.File_Handler import FileHandlerJson


def user_interaction():
    hh_api = HeadHunterAPI()
    file_handler = FileHandlerJson()

    while True:
        print("\nВыберете действие: ")
        print("1. Поиск вакансий по ключевому слову")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом из файла")
        print("4. Запись вакансий в файл")
        print("0. Выход")

        choice = input("Выберете действие: ")

        if choice == '1':
            keyword = input("Введите ключевое слово для поиска: ")
            amount = input("Введите количество вакансий для получения: ")

            try:
                vacancies = hh_api.load_vacancies(keyword, amount)
                print(vacancies)
            except Exception as error:
                print(f"произошла ошибка {error}")
        elif choice == '2':
            n = int(input("Введите количество вакансий для получения: "))
            vacancies = file_handler.get_vacancies()

            vacancies_with_salary = [
                vac for vac in vacancies
                if vac.get('salary') and isinstance(vac['salary'], dict)
                   and (vac['salary'].get('from') is not None or vac['salary'].get('to') is not None)
            ]
            sorted_vacancies = sorted(
                vacancies_with_salary,
                key=lambda x: max(
                    x['salary'].get('to', 0) or x['salary'].get('from', 0),
                    x['salary'].get('from', 0)
                ),
                reverse=True
            )[:n]

            if sorted_vacancies:
                for vacancy in sorted_vacancies:
                    area = vacancy.get('area', {})
                    city = area.get('name', 'Не указан') if isinstance(area, dict) else str(area)

                    salary = vacancy['salary']
                    salary_from = salary.get('from', '?')
                    salary_to = salary.get('to', '?')
                    currency = salary.get('currency', '')
                    gross = "(до вычета налогов)" if salary.get('gross') else "(на руки)"

                    print(f"""
                                Название: {vacancy['name']}
                                Город: {city}
                                Зарплата: {salary_from} - {salary_to} {currency} {gross}
                                Ссылка: {vacancy['url']}
                                """)
            else:
                print("Вакансий не найдено")
        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска в файле: ")
            vacancies = file_handler.get_vacancies(name=keyword)
            if vacancies:
                for vacancy in vacancies:
                    area = vacancy.get('area', {})
                    city = area.get('name', 'Не указан') if isinstance(area, dict) else str(area)

                    salary = vacancy['salary']
                    salary_from = salary.get('from', '?')
                    salary_to = salary.get('to', '?')
                    currency = salary.get('currency', '')
                    gross = "(до вычета налогов)" if salary.get('gross') else "(на руки)"

                    print(f"""
                                Название: {vacancy['name']}
                                Город: {city}
                                Зарплата: {salary_from} - {salary_to} {currency} {gross}
                                Ссылка: {vacancy['url']}
                                """)
            else:
                print("Вакансий не найдено")

        elif choice == '0':
            print("Выход из программы")
            break



if __name__ == "__main__":
    user_interaction()
