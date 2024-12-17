# --------------------------- Homework_15.1  ------------------------------------
# ------------------------ Демонстрація парсингу сайтика ----------------------------
"""
Виконав: Григорій Чернолуцький
Homework_15.1

парсингу сайтів із збереженням інформації до файлів різного формату
df.to_csv("output.csv")
df.to_excel("output.xlsx")
df.to_json("output.json")

Та  sqlite

Package Version
------- -------
pip 24.3.1

"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from dao import *
from package_parsing import scraping_minfin_com_ua

# Часовий період інформації для отримання вибіркового або максимально можливого обсягу даних
start_year = 2024  # мінімально можливий 1996 рік
end_year = 2024 + 1  # Повинно бути 2024 + 1
start_month = 1  # Повинно бути 1
end_month = 12 + 1  # Повинно бути 12 + 1
start_day = 1  # Повинно бути 1
end_day = 31 + 1  # Повинно бути 31 + 1
URL_BASE = "https://index.minfin.com.ua/ua/exchange/archive/nbu/"


def show_result_image(s, text) -> None:
    """
    Функція візуалізації дискретного ряду
    :param s: вхідний масив дискретних даних
    :param text: повідомлення
    :return: нічого
    """
    plt.plot(s)
    plt.ylabel(text)
    plt.show()
    return None


def save_to_files(data, file_name) -> None:
    df = pd.DataFrame(data)
    df.to_csv(f"output/{file_name}.csv")
    df.to_excel(f"output/{file_name}.xlsx")
    df.to_json(f"output/{file_name}.json")
    print("Дані збережені в файли")
    return None


def parsing_bank(caption_text) -> list:
    print(f"\nБеремо курс {caption_text} НБУ")
    rows = []
    for year in range(start_year, end_year):
        for month in range(start_month, end_month):
            for day in range(start_day, end_day):
                date = f"{str(year)}-{str(month):>02}-{str(day):>02}"
                URL_TEMPLATE = f"{URL_BASE}{date}/"
                print(f"Запит даних за {date}")
                scraping = scraping_minfin_com_ua(URL_TEMPLATE, caption_text)
                if scraping:
                    for scrap in scraping:
                        scrap.append(date)
                        rows.append(scrap)
    return rows


# Metal part -------------------------------------------------------------------------------------------->

def parsing_bank_metals(rows) -> dict:
    data = {'code': [], 'literal': [], 'name': [], 'price': [], 'delta': [], 'delta100': [], 'date': []}
    for row in rows:
        row.pop(3)
        print(row)
        data['code'].append(row[0])
        data['literal'].append(row[1])
        data['name'].append(row[2])
        data['price'].append(row[3])
        data['delta'].append(row[4])
        data['delta100'].append(row[5])
        data['date'].append(row[6])
    #      Можливо тут це ..... але імплементуємо це оптовим методом де інде
    #        insert_one_metal(row[0],row[1],row[2],row[3],row[4],row[5].replace(" %", ""),row[6])
    return data


def save_to_metal_db(data) -> None:
    n = len(data['code'])
    i = 0
    while i < n:
        insert_one_metal(data['code'][i], data['literal'][i], data['name'][i], data['price'][i],
                         data['delta'][i], data['delta100'][i].replace(" %", ""), data['date'][i])
        i += 1
    print("Дані збережені в DB")
    return


def scrapo_parsing_metal_main() -> None:
    rows = parsing_bank("металів")
    data = parsing_bank_metals(rows)
    save_to_files(data, "bank_metal")
    save_to_metal_db(data)
    return None


def show_metal_price(s):
    rows = get_all_metal_price_by_name(s)
    i = 0
    arr = np.zeros(len(rows))
    for row in rows:
        arr[i] = float(row[0].replace(",", ".")) / 31.10348
        i += 1
    show_result_image(arr, s)
    return None


def show_metals_price(metals):
    for metal in metals:
        show_metal_price(metal)


# Currency part ------------------------------------------------------------->

def parsing_bank_currency(rows):
    data = {'code': [], 'literal': [], 'count': [], 'name': [], 'price': [], 'delta': [], 'delta100': [], 'date': []}
    for row in rows:
        # row.pop(3)
        print(row)
        data['code'].append(row[0])
        data['literal'].append(row[1])
        data['count'].append(row[2])
        data['name'].append(row[3])
        data['price'].append(row[4])
        data['delta'].append(row[5])
        data['delta100'].append(row[6])
        data['date'].append(row[7])
    #      Можливо тут це ..... але імплементуємо це оптовим методом де інде
    #        insert_one_currency(row[0],row[1],row[2],row[3],row[4],row[5],row[6].replace(" %", ""),row[7])
    return data


def save_to_currency_db(data):
    n = len(data['code'])
    i = 0
    while i < n:
        insert_one_currency(data['code'][i], data['literal'][i], data['count'][i], data['name'][i], data['price'][i],
                            data['delta'][i], data['delta100'][i].replace(" %", ""), data['date'][i])
        i += 1
    print("Дані збережені в DB")


def scrapo_parsing_currency_main() -> None:
    rows = parsing_bank("валютний")
    data = parsing_bank_currency(rows)
    save_to_files(data, "currency")
    save_to_currency_db(data)
    return None


def show_currency_price(s) -> None:
    rows = get_all_currency_price_by_name(s)
    i = 0
    arr = np.zeros(len(rows))
    for row in rows:
        arr[i] = float(row[0].replace(",", "."))
        i += 1
    show_result_image(arr, s)
    return None


def show_currencies_price(currencies) -> None:
    for currency in currencies:
        show_currency_price(currency)
    return None


# --------------------------------- main module ----------------------------------------------
if __name__ == '__main__':
    init_db()
    # clear_all_metals()
    # scrapo_parsing_metal_main()
    show_metals_price(("Срібло", "Золото", "Платина", "Паладій"))

    # clear_all_currency()
    # scrapo_parsing_currency_main()
    show_currencies_price(("долар США", "Євро"))
    close_db()

''' 

Беремо курс металів НБУ
Запит даних за 2024-12-06
Офіційний курс банківських металів НБУ на 6.12.2024
Запит даних за 2024-12-07
Запит даних за 2024-12-08
Запит даних за 2024-12-09
Офіційний курс банківських металів НБУ на 9.12.2024
Запит даних за 2024-12-10
Офіційний курс банківських металів НБУ на 10.12.2024
Запит даних за 2024-12-11
Офіційний курс банківських металів НБУ на 11.12.2024
['959', 'XAU', 'Золото', '110324,4700', '+425.9200', '+0.388 %', '2024-12-06']
['961', 'XAG', 'Срібло', '1303,5200', '+29.3600', '+2.304 %', '2024-12-06']
['962', 'XPT', 'Платина', '39250,5700', '+280.4400', '+0.720 %', '2024-12-06']
['964', 'XPD', 'Паладій', '40700,6600', '+687.7100', '+1.719 %', '2024-12-06']
['959', 'XAU', 'Золото', '109336,2400', '-988.2300', '-0.896 %', '2024-12-09']
['961', 'XAG', 'Срібло', '1291,8700', '-11.6500', '-0.894 %', '2024-12-09']
['962', 'XPT', 'Платина', '38868,8200', '-381.7500', '-0.973 %', '2024-12-09']
['964', 'XPD', 'Паладій', '40430,0400', '-270.6200', '-0.665 %', '2024-12-09']
['959', 'XAU', 'Золото', '110228,3600', '+892.1200', '+0.816 %', '2024-12-10']
['961', 'XAG', 'Срібло', '1316,0400', '+24.1700', '+1.871 %', '2024-12-10']
['962', 'XPT', 'Платина', '39447,9500', '+579.1300', '+1.490 %', '2024-12-10']
['964', 'XPD', 'Паладій', '40980,8900', '+550.8500', '+1.362 %', '2024-12-10']
['959', 'XAU', 'Золото', '111411,7000', '+1183.3400', '+1.074 %', '2024-12-11']
['961', 'XAG', 'Срібло', '1327,1600', '+11.1200', '+0.845 %', '2024-12-11']
['962', 'XPT', 'Платина', '39270,4000', '-177.5500', '-0.450 %', '2024-12-11']
['964', 'XPD', 'Паладій', '40541,2300', '-439.6600', '-1.073 %', '2024-12-11']
Дані збережені в файли
Дані збережені в DB

'''
