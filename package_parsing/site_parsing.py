# ------------------ HTTP: для парсингу сайтів ----------------------------
"""

Приклад
парсингу сайтів із збереженням інформації до файлів різного формату
df.to_csv("output.csv")
df.to_excel("output.xlsx")
df.to_json("output.json")

Package                      Version
---------------------------- -----------
pip                          23.1
requests                     2.28.2
beautifulsoup4               4.12.3

"""

import requests
from bs4 import BeautifulSoup as bs


def parsing_site_bank_gav_ua(URL_TEMPLATE) -> dict:
    """
    site parsing python
    web scraping / site scraping python
    Data scraping - швидше очищення та підготовка даних
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html

    :param URL_TEMPLATE: URL Site work.ua
    :return: class 'dict'
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    '''
    Зміни в аргументі для методу get: headers=headers - МИ відрекомендувались звичайним браузером при зверненні до серверу.
    '''
    r = requests.get(URL_TEMPLATE, headers=headers)
    result_list = {'code': [], 'literal': [], 'count': [], 'name': [], 'course': []}
    soup = bs(r.text, "html.parser")
    exchange_code = soup.find_all('span', class_="value")
    exchange_literal = soup.find_all('td', attrs={"data-label": "Код літерний"})
    exchange_count = soup.find_all('td', attrs={"data-label": "Кількість одиниць валюти"})
    exchange_name = soup.find_all('td', attrs={"data-label": 'Назва валюти'})
    exchange_course = soup.find_all('td', attrs={"data-label": 'Офіційний курс'})
    constant = 0  # для балансування даних
    i = 0
    for code in exchange_code:
        i = i + 1
        if (i < (len(exchange_code) - constant)):
            result_list['code'].append(code.text)
    i = 0
    for literal in exchange_literal:
        i = i + 1
        if (i < (len(exchange_literal) - constant)):
            result_list['literal'].append(literal.text)

    i = 0
    for name in exchange_name:
        i = i + 1
        if (i < (len(exchange_name) - constant)):
            result_list['name'].append(name.text.replace("\n", "").replace("  ", ""))

    i = 0
    for count in exchange_count:
        i = i + 1
        if (i < (len(exchange_count) - constant)):
            result_list['count'].append(count.text)

    i = 0
    for course in exchange_course:
        i = i + 1
        if (i < (len(exchange_course) - constant)):
            result_list['course'].append(course.text)

    print(result_list['code'])
    print(result_list['literal'])
    print(result_list['count'])
    print(result_list['name'])
    print(result_list['course'])
    return result_list
