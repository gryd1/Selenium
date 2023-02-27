from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import pandas as pd
import os
import sqlite3
import csv


def security():
    # useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15")
    # options.add_argument("--proxy-server=51.89.157.175:8000")
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
    time.sleep(5)


def parsing_data():
    url = "https://fora.ua/"
    # Работа в фоновом режиме
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # Отключение режима вебдрайвера
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # Браузер во весь экран
    driver.maximize_window()
    # time.sleep(5)
    driver.implicitly_wait(3)
    # Закрыл окно оповещение
    driver.execute_script("document.getElementsByClassName('MuiButtonBase-root MuiButton-root jss19 MuiButton-text')[2].click()")
    # time.sleep(3)
    driver.implicitly_wait(3)
    # Заходим на все акции
    driver.execute_script("document.getElementsByTagName('span')[12].click()")
    time.sleep(3)
    driver.implicitly_wait(3)
    driver.execute_script("window.scrollTo(0, 2300);")
    time.sleep(50)
    driver.execute_script("document.getElementsByClassName('MuiButtonBase-root MuiButton-root jss244 MuiButton-text jss226')[0].click()")
    # driver.execute_script("document.getElementsByClassName('cl-floating-box-close-icon')[0].click()")
    time.sleep(3)
    # код парсинга
    soup = BS(driver.page_source, 'html.parser')
    product_name = soup.find_all('h2', class_='jss255')
    weight = soup.find_all('div', class_='jss256')
    base_price = soup.find_all('div', class_='jss260')
    promotional_price = soup.find_all('div', class_='jss261')
    validity = soup.find_all('div', class_='jss262')
    all_data = {'product_name': [], 'weight': [], 'base_price': [], 'promotional_price': [], 'validity': []}
    for item in product_name:
        item = (item.get_text("", strip=True))
        all_data['product_name'].append(item)
    for item in weight:
        item = (item.get_text("", strip=True))
        all_data['weight'].append(item)
    for item in base_price:
        item = (item.get_text("", strip=True))
        all_data['base_price'].append(item)
    for item in promotional_price:
        item = (item.get_text("", strip=True))
        all_data['promotional_price'].append(item)
    for item in validity:
        item = (item.get_text("", strip=True))
        all_data['validity'].append(item)
    n = len(os.listdir())
    df = pd.DataFrame(data=all_data)
    df.to_csv(f"product{n - 3}.csv", sep=';', index=False, encoding='cp1251')
    print(all_data)


def sqlite_data():
    global conn
    try:
        conn = sqlite3.connect('fora.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS promotion (product_name TEXT, weight TEXT, base_price TEXT, promotional_price TEXT, validity TEXT);""")
        conn.commit()
        print("Подключен к SQLite")
        sqlite_insert_query = """INSERT INTO promotion (product_name, weight, base_price, promotional_price, validity) VALUES (?, ?, ?, ?, ?);"""
        n = len(os.listdir())
        with open(f'product{n - 4}.csv', 'rt', encoding='cp1251') as g:
            document_data_ = csv.reader(g, delimiter=';')
            l_ = list(document_data_)
            ll = []
            for item in l_:
                item = tuple(item)
                ll.append(item)
        print(ll)
        cur.executemany(sqlite_insert_query, ll)
        conn.commit()
        print("Записи успешно вставлены в таблицу promotion", cur.rowcount)
        conn.commit()
        cur.execute("SELECT * FROM promotion;")
        all_results = cur.fetchall()
        print(all_results)
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")


parsing_data()
# sqlite_data()
