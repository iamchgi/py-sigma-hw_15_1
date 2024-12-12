# ------------------ HTTP: для парсингу сайтів ----------------------------
"""

Package                      Version
---------------------------- -----------
pip                          24.3.1
requests                     2.32.3
beautifulsoup4               4.12.3
pandas                       2.2.3
numpy                        2.2.0
openpyxl                     3.1.5

"""

import requests
from bs4 import BeautifulSoup as bs


def scraping_minfin_com_ua(URL_TEMPLATE, caption_text) -> list:
    """
    site parsing python
    web scraping / site scraping python
    Data scraping - швидше очищення та підготовка даних
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html

    Oz – тройська унція = 31.10348 грам

    :param URL_TEMPLATE: URL Site https://index.minfin.com.ua/ua/exchange/archive/nbu/
    :return: class 'dict'
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    '''
    Зміни в аргументі для методу get: headers=headers - МИ відрекомендувались звичайним браузером при зверненні до серверу.
    '''
    r = requests.get(URL_TEMPLATE, headers=headers)
    soup = bs(r.text, "html.parser")
    tables = soup.find_all("table")
    # table = soup.find("table", caption=lambda text: text and caption_text in text)
    result = []
    for table in tables:
        if table.find("caption") and table.find("caption").text and caption_text in table.find("caption").text:
            print(table.find("caption").text)
            rows = table.find_all("tr")  # Вилучення строк таблиці
            for row in rows:
                cells = row.find_all(["td"])  # Можливо как <td>, так и <th> але не треба поки  (["td", "th"])
                if cells:
                    result.append([cell.text.strip().replace("\xa0", " ") for cell in cells])
    return result
