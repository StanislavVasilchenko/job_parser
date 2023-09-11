import requests
import json
from abc import ABC, abstractmethod
from datetime import datetime


class ConnectAPI(ABC):

    @abstractmethod
    def get_area(self):
        """Получает список городов и регионов"""
        pass

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancy(self):
        """Ищет объявления о вакансиях по ключевым словам в указанном регионе.
        По умолчанию ищет во всех регионах"""
        pass


class HeadHunterVacancy(ConnectAPI):
    BASE_URL_VACANCY = "https://api.hh.ru/vacancies"
    BASE_URL_AREAS = "https://api.hh.ru/areas"

    def __init__(self, key_words):
        self.params = {
            "page": 0,
            "text": key_words,
            "area": 2,
            "per_page": 50
        }
        self.vacancy = []

    def get_area(self):
        """Записывает список городов в файл"""
        response_area = requests.get(self.BASE_URL_AREAS).json()
        return response_area

    def get_request(self):
        response = requests.get(self.BASE_URL_VACANCY, params=self.params)
        if response.status_code != 200:
            raise Exception(f"Code = {response.status_code}")
        return response.json()

    def get_vacancy(self):
        """Получение списка вакансий по ключевому слову"""
        page_count = self.get_request().get("pages")
        for page in range(page_count):
            self.params["page"] = page
            response = self.get_request().get('items')
            self.vacancy.extend(response)
            print(f"Count page = {page+1} / {page_count}")
        print(f"Найденно вакансий - {len(self.vacancy)}")
        return self.vacancy

    def get_new_format_vacancy(self):
        new_format = []
        for vacancy in self.vacancy:
            new_vacancy = {
                "id": vacancy["id"],
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

