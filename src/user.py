from src.vacancy import JobSearchApp


def user_interaction():
    """
     Запрашивает у пользователя ключ API, имя файла JSON, поисковый запрос, верхнее значение N и ключевое
    слово для взаимодействия с JobSearchApp и выполнения различных операций поиска вакансий.
     """
    api_key = input("Введите API ключ для hh.ru: ")
    json_filename = input("Введите имя файла для сохранения вакансий в формате JSON: ")
    job_app = JobSearchApp(api_key, json_filename)
    search_query = input("Введите поисковый запрос для запроса вакансий из hh.ru: ")
    job_app.search_and_save_vacancies(search_query)
    top_n = int(input("Введите количество вакансий для вывода топ N по зарплате: "))
    job_app.get_top_n_vacancies(top_n)
    keyword = input("Введите ключевое слово для поиска вакансий по описанию: ")
    job_app.search_vacancies_by_keyword(keyword)