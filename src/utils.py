from src.parser import HeadHunterVacancies, SuperJobVacancies
from src.file_worker import FileWorker


def site_selection(choice: int, key_words: str, city: str, api_key: str):
    """Получает на вход параметры от пользователя и загружает данные с выбранной платформы
    или с обеих сразу:
    choice: int - выбор платформы для загрузки данных,
    key_words: str - название профессии ключевое слово для поиска профессии,
    city: str - город в котором будет осуществляться поиск,
    api_key: str - ключ для работы с сервисом Super Job
    """
    if choice == 1:
        hh_vacancies = HeadHunterVacancies(key_words=key_words, city=city)
        return hh_vacancies.vacancy
    elif not api_key:
        print("Введите ключ что бы воспользоваться сервисом Super Job")
        quit()
    elif choice == 2:
        sj_vacancies = SuperJobVacancies(api_key, key_words, city)
        print(len(sj_vacancies.vacancy))
        return sj_vacancies.vacancy
    elif choice == 3:
        hh_vacancies = HeadHunterVacancies(key_words=key_words, city=city)
        sj_vacancies = SuperJobVacancies(api_key, key_words, city)
        return hh_vacancies + sj_vacancies


def user_interaction(vacancies: list):
    """На вход приходит список вакансий. Вакансии записываются в файл
    и осуществляется сценарий работы с пользователем.
    Пользователь может выбирать действия из предложенных:
    1 - Показать все вакансии
    2 - Вывести топ вакансий по ЗП
    3 - Выбрать вакансии по фильтру ЗП от - до
    4 - Найти вакансии по ключевому слову в требованиях к соискателю\n"
    5 - Выход
    """
    count_vacancies = len(vacancies)
    file_worker = FileWorker()
    file_worker.write_in_file(vacancies)
    while True:
        try:
            action = int(input(f"Выберите действие:\n"
                               f"1 - Показать все вакансии\n"
                               f"2 - Вывести топ вакансий по ЗП из {count_vacancies}\n"
                               f"3 - Выбрать вакансии по фильтру ЗП от - до\n"
                               f"4 - Найти вакансии по ключевому слову в требованиях к соискателю\n"
                               f"5 - Выход\n"
                               f"Ввод: "))
        except ValueError:
            print("Выбранный вариант должен быть числом. Повторите попытку")
            continue
        if action == 1:
            [print(vacancy) for vacancy in file_worker.get_top_vacancy(count_vacancies)]
        elif action == 2:
            try:
                top = int(input(f"Введите количество вакансий из {count_vacancies} - "))
            except ValueError:
                print("Выбранный вариант должен быть числом. Повторите попытку\n")
                continue
            while True:
                if top <= count_vacancies:
                    [print(vacancy) for vacancy in file_worker.get_top_vacancy(top)]
                    break
                else:
                    print(f"{top} больше чем число найденных вакансий\n"
                          f"Повторите попытку")
                    try:
                        top = int(input(f"Введите количество вакансий из {count_vacancies}"))
                    except ValueError:
                        print("Выбранный вариант должен быть числом. Повторите попытку\n")
                        continue
        elif action == 3:
            try:
                s_from, s_to = int(input("ОТ -")), int(input("ДО -"))
            except ValueError:
                print("Выбранный вариант должен быть числом. Повторите попытку\n")
                continue
            filtered_vacancy = file_worker.get_vacancy_by_salary(s_from, s_to)
            file_worker.get_top_vacancy(len(filtered_vacancy))
            [print(vacancy) for vacancy in filtered_vacancy]
        elif action == 4:
            key_words = input("Введите ключевое слово/слова для поиска в требованиях к соискателю: ").split(" ")
            vacancies_found = file_worker.get_vacancies_by_key_words(key_words)
            if len(vacancies_found):
                [print(vacancy) for vacancy in vacancies_found]
            else:
                print("По заданным параметрам вакансий не найдено\n")
        elif action == 5:
            quit()
        else:
            print("Выбран не верный вариант действий, повторите попытку")


def user_selection() -> int:
    """Выбор платформы для поиска вакансий
    1 - Head Hunter
    2 - Super Job
    3 - С обеих платформ
    """
    while True:
        try:
            choice = int(input("Выберите платформу с которой хотите загружать вакансии\n"
                               "1 - Head Hunter\n"
                               "2 - Super Job\n"
                               "3 - С обеих платформ\n"
                               "Введите вариант - "
                               ))
        except ValueError:
            print("\nВыбранный вариант должен быть числом. Повторите попытку\n")
            continue
        if choice not in range(1, 4):
            print("\nВыберите вариант от 1 до 3\n")
            continue
        return choice
