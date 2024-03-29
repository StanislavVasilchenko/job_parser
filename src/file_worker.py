import json
from abc import ABC, abstractmethod
from src.parser import Vacancy


class WorkingWithFile(ABC):

    @abstractmethod
    def read_from_file(self) -> json:
        """Считывает данные и файла и возвращает json"""
        pass

    @abstractmethod
    def write_in_file(self, vacancy) -> None:
        """Принимает на вход данные и записывает их в файл.
        По умолчанию имя файла vacancy.json"""
        pass

    @abstractmethod
    def get_top_vacancy(self, top) -> list[Vacancy]:
        """Получает на вход число вакансий top:int
        сортирует вакансии по размеру заработной платы от (если указанно),
        и возвращает список с объектами вакансий Vacancy"""
        pass

    @abstractmethod
    def get_vacancy_by_salary(self, s_from: int, s_to: int) -> list[Vacancy]:
        """Получает на вход два числа:
        s_from: int - диапазон поиска от,
        s_to: int - диапазон поиска до,
        выбирает вакансии в которых указана ЗП в заданном диапазоне ОТ и ДО,
        возвращает список с объектами вакансий Vacancy
        """
        pass

    @abstractmethod
    def get_vacancies_by_key_words(self, key_words: str) -> list[Vacancy]:
        """Получает на вход слово или несколько ключевых слов
        и ищет совпадение в полях описания вакансии
        возвращает список с объектами вакансий Vacancy
        """
        pass


class FileWorker(WorkingWithFile):
    def __init__(self, file_name: str = "vacancy.json"):
        self.file_name = file_name

    def read_from_file(self) -> json:
        with open(self.file_name, "r", encoding="utf-8") as file:
            result = json.load(file)
        return result

    def write_in_file(self, vacancy):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(vacancy, file, ensure_ascii=False, indent=4)

    def get_top_vacancy(self, top: int) -> list[Vacancy]:
        data = self.read_from_file()
        new_data = [Vacancy(**x) for x in data]
        for i in range(len(new_data)):
            for j in range(0, len(data) - 1):
                if new_data[j] > new_data[j + 1]:
                    new_data[j], new_data[j + 1] = new_data[j + 1], new_data[j]
        new_data = new_data[::-1]
        return new_data[:top]

    def get_vacancy_by_salary(self, s_from: int, s_to: int) -> list:
        data = self.read_from_file()
        filtered_vacancy = []
        for salary in data:
            if (salary.get("salary_from") in range(s_from, s_to + 1) and
                    salary.get("salary_to") in range(s_from, s_to + 1)):
                filtered_vacancy.append(Vacancy(**salary))
        return filtered_vacancy

    def get_vacancies_by_key_words(self, key_words: list) -> list:
        all_vacancies = self.read_from_file()
        vacancies_by_key_words = []
        for vacancy in all_vacancies:
            if vacancy.get("requirement") is not None:
                for word in key_words:
                    if word in vacancy.get("requirement"):
                        vacancies_by_key_words.append(Vacancy(**vacancy))

        return vacancies_by_key_words
