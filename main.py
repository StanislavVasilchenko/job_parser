from src.parser import HeadHunterVacancies, Vacancy
from src.file_worker import FileWorker


def main():
    key_words = input("Введите название профессии или ключевое слово поиска: ")
    city = input("Введите название города: ").title()
    hh_vacancies = HeadHunterVacancies(key_words=key_words, city=city)
    count_vacancies = len(hh_vacancies.vacancy)
    file_worker = FileWorker()
    file_worker.write_in_file(hh_vacancies.vacancy)
    while True:
        action = input(f"Выберите действие:\n"
                       f"1 - Показать все вакансии\n"
                       f"2 - Вывести топ вакансий по ЗП из {count_vacancies}\n"
                       f"3 - Выход\n"
                       f"Ввод: ")
        if action == "1":
            [print(vacancy) for vacancy in file_worker.get_top_vacancy(count_vacancies)]
        elif action == "2":
            top = int(input(f"Введите количество вакансий из {count_vacancies} - "))
            while True:
                if top <= count_vacancies:
                    [print(vacancy) for vacancy in file_worker.get_top_vacancy(top)]
                    break
                else:
                    print(f"{top} больше чем число найденных вакансий\n"
                          f"Повторите попытку")
                    top = int(input(f"Введите количество вакансий из {count_vacancies}"))
                    continue
        elif action == "3":
            break


if __name__ == "__main__":
    main()
