import requests
import json
from abc import ABC, abstractmethod
import os
from datetime import datetime


class ConnectAPI(ABC):

    @abstractmethod
    def get_area_requests(self):
        """Получает список городов и регионов"""
        pass

    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def get_vacancy(self):
        """Ищет объявления о вакансиях по ключевым словам в указанном регионе.
        По умолчанию ищет во всех регионах"""
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
        with open("all_areas.json", "w", encoding="utf-8") as file:
            json.dump(response_area, file, ensure_ascii=False, indent=4)
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
            if name_city == "Санкт-Петербург":
                return "2"
            if name_city in town.values():
                return town["id"]

    def get_requests(self):
        response = requests.get(self.BASE_URL_VACANCY, params=self.params)
        if response.status_code != 200:
            raise Exception(f"Code = {response.status_code}")
        return response.json()

    def get_vacancy(self):
        """Получение списка вакансий по ключевому слову"""
        vacancy = []
        page_count = self.get_requests().get("pages")
        for page in range(page_count):
            self.params["page"] = page
            response = self.get_requests().get('items')
            vacancy.extend(response)
            print(f"Count page = {page + 1} / {page_count}")
        print(f"Найденно вакансий - {len(vacancy)}")
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


class WorkingWithFile(ABC):

    @abstractmethod
    def read_from_file(self):
        pass

    @abstractmethod
    def write_in_file(self, vacancy):
        pass

    @abstractmethod
    def get_top_vacancy(self, top):
        pass

    @abstractmethod
    def deleter(self):
        pass


class Interaction(WorkingWithFile, ABC):
    def __init__(self, file_name: str = "vacancy.json"):
        self.file_name = file_name

    def read_from_file(self):
        with open(self.file_name, "r", encoding="utf-8") as file:
            result = json.load(file)
        return result

    def write_in_file(self, vacancy):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(vacancy, file, ensure_ascii=False, indent=4)

    def get_top_vacancy(self, top):
        data = self.read_from_file()
        new_data = [Vacancy(**x) for x in data]
        for i in range(len(new_data)):
            for j in range(0, len(data)-1):
                if new_data[j] > new_data[j+1]:
                    new_data[j], new_data[j+1] = new_data[j+1], new_data[j]
        new_data = new_data[::-1]
        return new_data[:top]

    def deleter(self):
        pass


a = HeadHunterVacancies("python developer", "Волгоград")
# path = "/job_parser/file/vac.json"
# with open(path, "w", encoding="utf-8") as file:
#     json.dump(a.vacancy, file, ensure_ascii=False, indent=4)
b = Interaction()
k = b.get_top_vacancy(5)
[print(x) for x in k]
