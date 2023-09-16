import json
from abc import ABC, abstractmethod
from src.parser import Vacancy


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


class FileWorker(WorkingWithFile):
    def __init__(self, file_name: str = "../vacancy.json"):
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
            for j in range(0, len(data) - 1):
                if new_data[j] > new_data[j + 1]:
                    new_data[j], new_data[j + 1] = new_data[j + 1], new_data[j]
        new_data = new_data[::-1]
        return new_data[:top]

    def get_vacancy_by_salary(self, s_from: int, s_to: int):
        data = self.read_from_file()
        filtered_vacancy = []
        for i in data:
            if i.get("salary_from") in range(s_from, s_to+1) and i.get("salary_to") in range(s_from, s_to+1):
                filtered_vacancy.append(Vacancy(**i))
        [print(vac) for vac in filtered_vacancy]

    def deleter(self):
        pass

# a = FileWorker()
# a.get_vacancy_by_salary(30000, 100000)