import requests
from bs4 import BeautifulSoup
import re
import csv
import os


URL = ''
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36' , 'accept': '*/*'}
FILE = 'cars.csv'


def get_html(url,params = None):
    result = requests.get(url, headers=HEADERS, params=params)
    return result


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="ListingItem-module__main")


    cars = []
    for item in items:
        pricee = re.findall(r'\d', item.find('div', class_="ListingItemPrice-module__content").get_text())
        price = "".join(pricee)
        cars.append({
            'title': item.find('h3', class_="ListingItemTitle-module__container ListingItem-module__title").get_text(),
            'link': item.find('a', class_='Link ListingItemTitle-module__link').get('href'),
            'price': price,
        })

    return cars


def save_file(items, path):
    with open(path, 'w', newline='', decode='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Cсылка', 'Цена'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    cars = []
    while True:
        try:
            pages_count = int(input('Введите количество страниц: '))
        except:
            print('Пожалуйста , введите целое число...')
            continue
        else:
            print('Выполняется парсинг!')
            break

    for page in range(1, pages_count + 1):
        print(f'Парсинг страницы {page} из {pages_count}...')
        html = get_html(URL, params={'page': page })
        cars.extend(get_content(html.text))
        save_file(cars,FILE)

    print(cars)
    print(f'Получено {len(cars)} автомобилей')
    os.startfile(FILE)

parse()

