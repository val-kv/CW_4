import json
import requests

from abc import ABC, abstractmethod


class AbstractVacancyAPI(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HhVacancyAPI(AbstractVacancyAPI):

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://api.hh.ru/vacancies'

    def connect(self):
        # Implement logic to connect to the hh.ru API using the provided API key
        pass

    def get_vacancies(self):
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': 'Python Developer',
            'area': 1,
            'only_with_salary': True,
            'per_page': 10
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            vacancies = response.json()
            return vacancies['items']
        else:
            return []

    def get_vacancies_by_criteria(self, search_query):
        # Implement logic to retrieve vacancies by criteria
        pass


class Vacancy:

    def __init__(self, title, link, salary, description):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description
        self.validate_data()

    def validate_data(self):
        if not self.salary:
            self.salary = "Зарплата не указана"

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary


class AbstractVacancySaver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_criteria(self, criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(AbstractVacancySaver):

    def __init__(self, filename):
        self.filename = filename
        self.vacancies = []

    def add_vacancy(self, vacancy):
        self.vacancies.append(vars(vacancy))

    def get_vacancies_by_criteria(self, criteria):
        # Implement logic to retrieve vacancies by criteria
        pass

    def delete_vacancy(self, vacancy):
        self.vacancies = [v for v in self.vacancies if v != vars(vacancy)]

    def save_to_json(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)



class JobSearchApp:

    def __init__(self, api_key, json_filename):
        self.api = HhVacancyAPI(api_key)
        self.saver = JSONSaver(json_filename)

    def search_and_save_vacancies(self, search_query, json_filename=None):
        self.api.connect()
        vacancies = self.api.get_vacancies()
        for vacancy in vacancies:
            title = vacancy['name']
            url = f"https://hh.ru/vacancy/{vacancy['id']}"
            salary = f"{vacancy['salary']['from']} - {vacancy['salary']['to']}"
            snippet = vacancy['snippet']['requirement']
            vacancy_dict = Vacancy(title, url, salary, snippet)
            self.saver.add_vacancy(vacancy_dict)
        self.saver.save_to_json()

    def get_top_n_vacancies(self, n):
        # Implement logic to retrieve top N vacancies by salary
        pass

    def search_vacancies_by_keyword(self, keyword):
        # Implement logic to search vacancies by keyword in the description
        pass


def user_interaction():
    api_key = input("Введите API ключ для hh.ru: ")
    json_filename = input("Введите имя файла для сохранения вакансий в формате JSON: ")
    job_app = JobSearchApp(api_key, json_filename)
    search_query = input("Введите поисковый запрос для запроса вакансий из hh.ru: ")
    job_app.search_and_save_vacancies(search_query)
    top_n = int(input("Введите количество вакансий для вывода топ N по зарплате: "))
    job_app.get_top_n_vacancies(top_n)
    keyword = input("Введите ключевое слово для поиска вакансий по описанию: ")
    job_app.search_vacancies_by_keyword(keyword)


user_interaction()
