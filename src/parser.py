import json

import requests
from abc import ABC, abstractmethod
import os


class ConnectAPI(ABC):

    # @abstractmethod
    # def get_area_requests(self):
    #     """Получает список городов и регионов"""
    #     pass
    #
    @abstractmethod
    def get_requests(self):
        """Подключается к сервису с вакансиями"""
        pass

    @abstractmethod
    def get_vacancy(self):
        """Получает вакансии"""
        pass

    @abstractmethod
    def get_new_format_vacancy(self):
        """Форматирует список вакансий к виду:
        "vacancy_id": id,
        "name": Название вакансии,
        "salary_from": Оклад от, если указан,
        "salary_to": Оклад до, если указан,
        "currency": Название валюты,
        "url": Ссылка на вакансию,
        "employer": Наименование работодателя,
        "requirement": Требования к соискателю,
        "responsibility": Краткое описание должностных обязанностей"""
        pass


class HeadHunterVacancies(ConnectAPI):
    BASE_URL_VACANCY = "https://api.hh.ru/vacancies"
    BASE_URL_AREAS = "https://api.hh.ru/areas"

    def __init__(self, key_words, city):
        self.params = {
            "page": 0,
            "text": key_words,
            "area": self.get_id_city(city),
            "per_page": 50
        }
        self.vacancy = self.get_new_format_vacancy()

    def get_area_requests(self):
        """Записывает список городов в файл"""
        response_area = requests.get(self.BASE_URL_AREAS).json()[0].get("areas")
        cities = []
        for district in response_area:
            for town in district["areas"]:
                area = {
                    "id": town["id"],
                    "name": town["name"]
                }
                cities.append(area)
        return cities

    def get_id_city(self, name_city: str):
        cities = self.get_area_requests()
        for town in cities:
            if name_city == "Москва":
                return "1"
            elif name_city == "Санкт-Петербург":
                return "2"
            elif name_city in town.values():
                return town["id"]

    def get_requests(self):
        response = requests.get(self.BASE_URL_VACANCY, params=self.params)
        if response.status_code != 200:
            raise Exception(f"Code = {response.status_code}")
        return response.json()

    def get_vacancy(self):
        vacancy = []
        page_count = self.get_requests().get("pages")
        for page in range(page_count):
            self.params["page"] = page
            response = self.get_requests().get('items')
            vacancy.extend(response)
        print(f"Найдено вакансий - {len(vacancy)}")
        return vacancy

    def get_new_format_vacancy(self):
        new_format = []
        response = self.get_vacancy()
        for vacancy in response:
            new_vacancy = {
                "vacancy_id": vacancy["id"],
                "name": vacancy["name"],
                "salary_from": vacancy["salary"]["from"] if vacancy["salary"] else None,
                "salary_to": vacancy["salary"]["to"] if vacancy["salary"] else None,
                "currency": vacancy["salary"]["currency"] if vacancy["salary"] else None,
                "url": vacancy["alternate_url"],
                "employer": vacancy["employer"]["name"],
                "requirement": vacancy["snippet"]["requirement"],
                "responsibility": vacancy["snippet"]["responsibility"]
            }
            new_format.append(new_vacancy)
        return new_format


class SuperJobVacancies(ConnectAPI):
    API_KEY = os.getenv("SJ_API_KEY")
    BASE_URL_VACANCY = "https://api.superjob.ru/2.0/vacancies/"
    BASE_URL_AREAS = "	https://api.superjob.ru/2.0/towns/"

    def __init__(self, key_words, city):
        self.params = {
            "town": city,
            "keyword": key_words,
            "page": 0,

        }
        self.headers = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": self.API_KEY,
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        # self.vacancy = self.get_new_format_vacancy()
    # def get_area_requests(self):
    #     params = {
    #         "X-Api-App-Id": self.API_KEY,
    #         "town": "Ставрополь"
    #     }
    #     responce = requests.get(self.BASE_URL_AREAS, params=params).json()
    #     with open("SJareas.json", "w", encoding="utf-8") as file:
    #         json.dump(responce, file, ensure_ascii=False, indent=4)

    def get_requests(self):
        response = requests.get(self.BASE_URL_VACANCY, params=self.params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Code = {response.status_code}")
        # with open("SJareas.json", "w", encoding="utf-8") as file:
        #     json.dump(response.json(), file, ensure_ascii=False, indent=4)
        return response.json()

    def get_vacancy(self):
        pass

    def get_new_format_vacancy(self):
        pass


class Vacancy:
    def __init__(self, vacancy_id: str = "", name: str = "", salary_from: int = 0, salary_to: int = 0,
                 currency: str = "", url: str = "", employer: str = "", requirement: str = "",
                 responsibility: str = ""):
        self.vacancy_id = vacancy_id
        self.name = name
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else "Не указано"
        self.currency = currency if currency is not None else ""
        self.url = url
        self.employer = employer
        self.requirement = requirement
        self.responsibility = responsibility

    def __str__(self):
        return (f"id - {self.vacancy_id}\n"
                f"Вакансия - {self.name}\n"
                f"Заработная плата от {self.salary_from} до {self.salary_to} {self.currency}\n"
                f"Ссылка на вакансию - {self.url}\n"
                f"Работодатель - {self.employer}\n"
                f"Требования к соискателю - {self.requirement}\n"
                f"Обязанности - {self.responsibility}\n")

    def __gt__(self, other):
        if self.salary_from and other.salary_from is not None:
            return self.salary_from > other.salary_from

    def __lt__(self, other):
        if self.salary_from and other.salary_from is not None:
            return self.salary_from < other.salary_from


a = SuperJobVacancies("Программист", "Москва")
a.get_requests()