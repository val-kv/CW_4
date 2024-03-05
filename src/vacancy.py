from typing import List

from pip._vendor import requests
from src.abstract import HhVacancyAPI
from src.json_saver import JSONSaver


class Vacancy:

    def __init__(self, title, link, salary, description):
        """
         Инициализирует объект с предоставленным названием, ссылкой, зарплатой и описанием.
         """
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description
        self.validate_data()

    def validate_data(self):
        """
         Проверьте данные и установите значение по умолчанию для зарплаты, если оно не указано.
        """
        if not self.salary:
            self.salary = "Зарплата не указана"

    def __le__(self, other):
        """
        Сравните диапазон зарплат текущего объекта с другим объектом и верните значение True, если
        текущий диапазон зарплат меньше или равен диапазону зарплат другого объекта.
        Если во время сравнения возникает исключение, верните значение None.
        """
        try:
            salary_from, salary_to = self.salary.split('-')
            salary_from_other, salary_to_other = other.salary.split('-')
            if salary_to != 'None' and salary_from != 'None':
                return (int(salary_to) + int(salary_from) / 2) <= (int(salary_to_other) + int(salary_from_other) / 2)
            elif salary_to == 'None' and salary_from != 'None':
                return int(salary_from) <= int(salary_from_other)
            elif salary_to != 'None' and salary_from == 'None':
                return int(salary_to) <= int(salary_to_other)
            else:
                return int(salary_to) <= int(salary_to_other)
        except:
            return

    def __lt__(self, other):
        """
        Сравнивает зарплату self с зарплатой другого объекта.
        Возвращает значение True, если среднее значение диапазона зарплат self меньше
        среднего значения диапазона зарплат другого объекта. Возвращает значение False, если диапазон
        зарплат self выше или равен диапазону зарплат другого объекта.
        Если во время сравнения возникает исключение, None не возвращается.
        """
        try:
            salary_from, salary_to = self.salary.split('-')
            salary_from_other, salary_to_other = other.salary.split('-')
            if salary_to != 'None' and salary_from != 'None':
                return (int(salary_to) + int(salary_from) / 2) < (int(salary_to_other) + int(salary_from_other) / 2)
            elif salary_to == 'None' and salary_from != 'None':
                return int(salary_from) < int(salary_from_other)
            elif salary_to != 'None' and salary_from == 'None':
                return int(salary_to) < int(salary_to_other)
            else:
                return int(salary_to) < int(salary_to_other)
        except:
            return

    def compare_salary(self, other_vacancy):
        """
        Сравнивает зарплату между двумя вакансиями и возвращает результат в виде строкового сообщения.
         """
        if self.salary == "Зарплата не указана" or other_vacancy.salary == "Зарплата не указана":
            return "Сравнение невозможно из-за отсутствия информации о зарплате"
        self_salary = self.salary.replace(' ', '')
        other_salary = other_vacancy.salary.replace(' ', '')
        self_salary = self.extract_salary(self_salary)
        other_salary = self.extract_salary(other_salary)
        if self_salary < other_salary:
            return f"{self.title} имеет меньшую зарплату, чем {other_vacancy.title}"
        elif self_salary > other_salary:
            return f"{self.title} имеет большую зарплату, чем {other_vacancy.title}"
        else:
            return f"Зарплаты вакансий {self.title} и {other_vacancy.title} равны"

    @staticmethod
    def extract_salary(salary):
        """
        Извлекает среднюю заработную плату из заданного диапазона заработной платы или указанного значения заработной платы.
        :param salary: Входная строка заработной платы, подлежащая обработке.
        :return: Извлеченное значение средней заработной платы.
        """
        salary = salary.split('-')
        if len(salary) == 2:
            return (int(salary[0]) + int(salary[1])) / 2
        elif 'от' in salary[0]:
            return int(salary[0].replace('от', ''))
        elif 'до' in salary[0]:
            return int(salary[0].replace('до', ''))
        else:
            return int(salary[0].replace('до', ''))


class JobSearchApp:

    def __init__(self, api_key, json_filename):
        self.url = 'https://api.hh.ru/vacancies'
        self.api = HhVacancyAPI(api_key)
        self.saver = JSONSaver(json_filename)

    def search_and_save_vacancies(self, search_query):
        """
         Инициализируйте класс с помощью предоставленного API-ключа и имени файла JSON.
         Параметры:
         api_key (str): Ключ API для доступа к HhVacancyAPI.
         json_filename (str): Имя файла для сохранения данных в формате JSON.
         Возвращается:
         None
        """
        self.api.connect()
        vacancies = self.api.get_vacancies(params={'text': search_query})
        for vacancy in vacancies:
            title = vacancy['name']
            url = f"https://hh.ru/vacancy/{vacancy['id']}"
            salary = vacancy['salary']
            snippet = vacancy['snippet']['requirement']
            vacancy_dict = Vacancy(title, url, salary, snippet)
            self.saver.add_vacancy(vacancy_dict)
        self.saver.save_to_json()

    def get_top_n_vacancies(self, n):
        pass

    def search_vacancies_by_keyword(self, keyword):
        pass

    def get_vacancies_by_criteria(self, params, search_query: str, ) -> List[Vacancy]:
        """
        Отправляет запрос GET в API и возвращает список вакансий.
        :param search_query:
        :param params: Параметры, которые должны быть переданы в запросе.
        :return: Список вакансий.
        """
        params = {
            'text': search_query,
            'area': 1,
            'only_with_salary': True,
            'per_page': 10
        }
        response = requests.get(f"{self.url}", params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            return []
