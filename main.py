from src.File_Handler import FileHandlerJson
from src.HH_API import HeadHunterAPI
from src.Vacancy import Vacancy


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    print("Добро пожаловать в приложение по поиску вакансий!")

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для загрузки: "))
    filter_words = input(
        "Введите ключевые слова для фильтрации через пробел или оставьте пустым: "
    ).split()
    salary_range_input = input("Введите диапазон зарплат или оставьте пустым: ")

    hh_api = HeadHunterAPI()
    vacancy = hh_api.get_vacancies(search_query, per_page=top_n)

    vacancies_list = Vacancy.cast_to_object_list(vacancy)
    print(f"Загружено {len(vacancies_list)} вакансий.")

    saver = FileHandlerJson()
    saver.save_to_json(vacancies_list)

    if filter_words:
        keyword_query = " ".join(filter_words)
        print(f"\n=== Фильтрация по ключевым словам: '{keyword_query}' ===")
        filtered_by_keyword = saver.filter_vacancies_by_keyword(keyword_query)
        for v in filtered_by_keyword:
            print(v)

    if salary_range_input:
        print(f"\n=== Фильтрация по зарплате: {salary_range_input} ===")
        try:
            filtered_by_salary = saver.filter_vacancies_by_salary_range(salary_range_input)
            for v in filtered_by_salary:
                print(v)
        except ValueError as e:
            print(e)

    print("\n=== Все вакансии после обработки ===")
    all_vacancies = saver.load_vacancies()
    for v in all_vacancies:
        print(v)

    while True:
        sort_choice = input("\nХотите отсортировать вакансии по зарплате? (да/нет): ").lower()
        if sort_choice == "нет":
            print("Сортировка не совершена")
            break
        elif sort_choice == "да":
            while True:
                reverse_choice = input("Сортировать по возрастанию (в) или убыванию (у)? ").lower()
                if reverse_choice == "в":
                    reverse = False
                    break
                elif reverse_choice == "у":
                    reverse = True
                    break
                else:
                    print("Введите пожалуйста только 'в' (возрастание) или 'y' (убывание)!")

            sorted_vacancies = Vacancy.sort_vacancies_by_salary(all_vacancies, reverse=reverse)
            print("\n=== Отсортированные вакансии ===")
            for v in sorted_vacancies:
                print(v)
            break
        else:
            print("Введите пожалуйста только 'да' или 'нет'!")


if __name__ == "__main__":
    user_interaction()
