import json

from abc import ABC, abstractmethod


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
        """
        Инициализирует объект с указанным именем файла.
        :param filename:
        """
        self.filename = filename
        self.vacancies = []

    def add_vacancy(self, vacancy):
        """
        Добавляет вакансии в список вакансий.
        :param vacancy:
        :return:
        """
        self.vacancies.append(vars(vacancy))

    def get_vacancies_by_criteria(self, criteria):
        pass

    def delete_vacancy(self, vacancy):
        """
        Удаляет вакансии из списка вакансий.
        :param vacancy:
        :return:
        """
        self.vacancies = [v for v in self.vacancies if v != vars(vacancy)]

    def save_to_json(self):
        """
        Сохраняет данные вакансий в файл JSON.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)