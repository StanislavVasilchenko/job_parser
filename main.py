import os
from src.utils import site_selection, user_interaction, user_selection


def main():
    sj_api_key = os.getenv("SJ_API_KEY")
    choice = user_selection()
    key_words = input("Введите название профессии или ключевое слово поиска: ").title()
    city = input("Введите название города: ").title()
    vacancies = site_selection(choice, key_words, city, sj_api_key)
    count_vacancies = len(vacancies)
    if count_vacancies == 0:
        print("По данному запросу вакансий не найдено")
        quit()
    print(f"Найденно вакансий - {len(vacancies)}")

    user_interaction(vacancies)


if __name__ == "__main__":
    main()
