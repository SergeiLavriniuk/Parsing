import csv
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup

CSV = 'data.csv'

HOST = 'https://www.marko.by'
URL = 'https://www.marko.by/muzhchinam/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

#запрос
def get_html(url):
    responce = requests.get(url=url, headers=HEADERS)
    return responce

#парсим контент
def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='prod')
    cards = []

    for item in items:
        cards.append(
            {
                'code': item.find('div', class_='prod__code').get_text(strip=True),
                'prod_link': HOST + item.find('a', class_='prod__inner').get('href'),
                'card_img': HOST + item.find('picture').find('img').get('src'),
                'sizes': item.find('div', class_='prod__title prod__desc prod__size').get('all_sizes'),
                'price': item.find('div', class_='prod__foot').find('div', class_='prod__price').find('div', class_='prod__price__cur').get_text(strip=True),
            }
        )
    return cards

# html = get_html(URL)     #проверочный код
# print(get_content(html.text))

def parser_data():
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, 39):
            url = f'https://www.marko.by/muzhchinam/?PAGEN_1={page}&count=36'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')

            items = soup.find_all('div', class_='prod')

            for item in items:
                cards.append(
                    {
                        'code' : item.find('div', class_='prod__code').get_text(strip=True),
                        'link': HOST + item.find('a', class_='prod__inner').get('href'),
                        'card_image': HOST + item.find('picture').find('img').get('src'),
                        'sizes': item.find('div', class_='prod__title prod__desc prod__size').get('all_sizes'),
                        'price' : item.find('div', class_='prod__foot').find('div', class_='prod__price').find('div', class_='prod__price__cur').get_text(strip=True)
                    }
                )
        # print(cards) проверяем карточки
        with open('results.json', 'w') as file:
            json.dump(cards, file, indent=4, ensure_ascii=False)

if __name__=='__main__':
    parser_data()