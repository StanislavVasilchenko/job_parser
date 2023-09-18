from src.parser import HeadHunterVacancies, SuperJobVacancies


def site_selection(choice: int, key_words: str, city: str, api_key=None,):
    if choice == 2 or 3 and api_key is None:
        return
    if choice == 1:
        hh_vacancies = HeadHunterVacancies(key_words=key_words, city=city)
        return hh_vacancies.vacancy
    elif choice == 2:
        sj_vacancies = SuperJobVacancies(api_key, key_words, city)
        print(len(sj_vacancies.vacancy))
        return sj_vacancies.vacancy
    elif choice == 3:
        hh_vacancies = HeadHunterVacancies(key_words=key_words, city=city)
        sj_vacancies = SuperJobVacancies(api_key, key_words, city)
        return hh_vacancies + sj_vacancies
