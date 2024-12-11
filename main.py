# --------------------------- Homework_6.1  ------------------------------------
"""
Виконав: Григорій Чернолуцький
Homework_15.1


Package Version
------- -------
pip 24.3.1

"""
import pandas as pd
import dao.grud
from dao.grud import insert_one_metal
from package_parsing import (
    parsing_minfin_com_ua
)

def package_parsing_main_def() -> None:
    data = {'code': [], 'literal': [], 'name': [], 'price': [],'delta': [],'delta100': [], 'date' : []}
    print("\nКурс металів НБУ")
    URL_BASE = "https://index.minfin.com.ua/ua/exchange/archive/nbu/"
    for year in range(2023,2025):
        for month in range(12,13):
            for day in range(19,32):
                date = f"{str(year)}-{str(month):>02}-{str(day):>02}"
                URL_TEMPLATE = f"{URL_BASE}{date}/"
                print(f"Запит даних за {date}")
                scraping = parsing_minfin_com_ua(URL_TEMPLATE, caption_text ="металів")
                for row in scraping:
                    row.pop(3)
                    print(row)
                    data['code'].append(row[0])
                    data['literal'].append(row[1])
                    data['name'].append(row[2])
                    data['price'].append(row[3])
                    data['delta'].append(row[4])
                    data['delta100'].append(row[5])
                    data['date'].append(date)
                    insert_one_metal(row[0],row[1],row[2],row[3],row[4],row[5],date)

    df = pd.DataFrame(data)
    df.to_csv("output/exchange.csv")
    df.to_excel("output/exchange.xlsx")
    df.to_json("output/exchange.json")
    print("Дані збережені в файли")
    return


def main() -> None:
    # ------------------------ Демонстрація парсингу сайтика ----------------------------
    package_parsing_main_def()


# --------------------------------- main module ----------------------------------------------
if __name__ == '__main__':
    main()

''' 


Курс НБУ
['036', '944', '933', '975', '410', '344', '208']
['AUD', 'AZN', 'BYN', 'BGN', 'KRW', 'HKD', 'DKK']
['1', '1', '1', '1', '100', '1', '1']
[' Австралійський долар ', ' Азербайджанський манат ', ' Білоруський рубль ', ' Болгарський лев ', ' Вона ', ' Гонконгівський долар ', ' Данська крона ']
['27,2243', '24,3960', '15,0684', '22,6710', '2,9572', '5,3312', '5,9457']

'''
