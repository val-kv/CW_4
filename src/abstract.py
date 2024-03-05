
from abc import ABC, abstractmethod
from typing import List

from pip._vendor import requests


class AbstractVacancyAPI(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self, params):
        pass


class HhVacancyAPI(AbstractVacancyAPI):

    def __init__(self, api_key):
        """
        Инициализирует объект с указанным именем файла.
        :param api_key:
        """
        self.api_key = api_key
        self.url = 'https://api.hh.ru/vacancies'

    def connect(self):
        # Implement logic to connect to the hh.ru API using the provided API key
        pass

    def get_vacancies(self, params):
        """
        Отправляет запрос GET в API и возвращает список вакансий.
        :param params: Параметры, которые должны быть переданы в запросе.
        :return: Список вакансий.
        """
        response = requests.get(f"{self.url}", params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            return None

    #def get_vacancies(self):
        #url = 'https://api.hh.ru/vacancies'
        #params = {
            #'text': 'Python Developer',
            #'area': 1,
            #'only_with_salary': True,
            #'per_page': 10
        #}
        #response = requests.get(url, params=params)
        #if response.status_code == 200:
            #vacancies = response.json()
            #return vacancies['items']
        #else:
            #return []



