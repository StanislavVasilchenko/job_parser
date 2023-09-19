import json
from src.exceptions import FailedConnection
import requests
from abc import ABC, abstractmethod


class ConnectAPI(ABC):

    @abstractmethod
    def get_requests(self):
        """Подключается к сервису с вакансиями"""
        pass

    @abstractmethod
    def get_vacancy(self):
        """Получает вакансии и возвращает список"""
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
    """Класс для работы с сервисом Head Hunter"""
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

    def get_area_requests(self) -> list[dict]:
        """Получает список городов и их id"""
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

    def get_id_city(self, name_city: str) -> str:
        """Принимает на вход название города и возвращает его id"""
        cities = self.get_area_requests()
        for town in cities:
            if name_city == "Москва":
                return "1"
            elif name_city == "Санкт-Петербург":
                return "2"
            if name_city in town.values():
                return town["id"]

    def get_requests(self) -> json:
        response = requests.get(self.BASE_URL_VACANCY, params=self.params)
        if response.status_code != 200:
            raise FailedConnection(f"Ошибка запроса! Статус ответа: {response.status_code}")
        return response.json()

    def get_vacancy(self) -> list[dict]:
        vacancy = []
        page_count = self.get_requests().get("pages")
        for page in range(page_count):
            self.params["page"] = page
            response = self.get_requests().get('items')
            vacancy.extend(response)
        return vacancy

    def get_new_format_vacancy(self) -> list[dict]:
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

    def __add__(self, other):
        return self.vacancy + other.vacancy

    def __len__(self):
        return len(self.vacancy)


class SuperJobVacancies(ConnectAPI):
    """Класс для работы с сервисом Super Job"""
    BASE_URL_VACANCY = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, secret_key, key_words, city):
        self.secret_key = secret_key
        self.params = {
            "town": city,
            "keyword": key_words,
            "page": 0
        }
        self.headers = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": self.secret_key,
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.vacancy = self.get_new_format_vacancy()

    def get_requests(self) -> json:
        response = requests.get(self.BASE_URL_VACANCY, params=self.params, headers=self.headers)
        if response.status_code != 200:
            raise FailedConnection(f"Ошибка запроса! Статус ответа: {response.status_code}")
        return response.json()

    def get_vacancy(self) -> list[dict]:
        all_vacancies = []
        for page in range(100):
            self.params["page"] = page
            if self.get_requests().get("more"):
                vacancies = self.get_requests()["objects"]
                all_vacancies.extend(vacancies)
            else:
                break
        return all_vacancies

    def get_new_format_vacancy(self) -> list[dict]:
        new_format = []
        response = self.get_vacancy()
        for vacancy in response:
            new_vacancy = {
                "vacancy_id": vacancy["id"],
                "name": vacancy["profession"],
                "salary_from": vacancy["payment_from"],
                "salary_to": vacancy["payment_to"],
                "currency": vacancy["currency"],
                "url": vacancy["link"],
                "employer": vacancy["client"].get("title"),
                "requirement": vacancy["candidat"] if not None else " ",
                "responsibility": vacancy["vacancyRichText"]
            }
            new_format.append(new_vacancy)
        return new_format

    def __add__(self, other):
        return self.vacancy + other.vacancy

    def __len__(self):
        return len(self.vacancy)


class Vacancy:
    """Класс для работы с вакансиями"""

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
        self.requirement = requirement if requirement is not None else " "
        self.responsibility = responsibility

    def __str__(self):
        return (f"id - {self.vacancy_id}\n"
                f"Вакансия - {self.name}\n"
                f"Заработная плата от {self.salary_from if self.salary_from != 0 else 'Не указано'}"
                f" до {self.salary_to} {self.currency}\n"
                f"Ссылка на вакансию - {self.url}\n"
                f"Работодатель - {self.employer}\n"
                f"Требования к соискателю - {self.requirement.strip()}\n"
                f"Обязанности - {self.responsibility}\n")

    def __gt__(self, other):
        if self.salary_from and other.salary_from is not None:
            return self.salary_from > other.salary_from

    def __lt__(self, other):
        if self.salary_from and other.salary_from is not None:
            return self.salary_from < other.salary_from
