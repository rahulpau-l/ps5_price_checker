import requests
import json
import csv
from bs4 import BeautifulSoup
from datetime import date

headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36'
    }

def newegg_price() -> (str, str):
    r = requests.get(json_data['newegg_url'],headers=headers)
    text = r.text.encode('utf-8').decode('ascii', 'ignore')
    soup = BeautifulSoup(text, features='html.parser')

    title = soup.title.string
    price = (f"${soup.find('span', class_='price').string}")
    in_stock = soup.find('span', class_='availability').string
    currency = soup.find('span', class_='price_currency_code').string


    print(title)
    print("Price:", price)
    print("Currency:", currency)
    print("In Stock:", is_it_in_stock(in_stock))

    return (title, price)

def bestbuy_price() -> (str, str):
    r = requests.get(json_data['bestbuy_url'], headers=headers)
    text = r.text.encode('utf-8').decode('ascii', 'ignore')

    soup = BeautifulSoup(text, features='html.parser')

    title = soup.title.string
    print("Title:", title)
    #getting the price
    price = soup.find('div', class_='price_FHDfG large_3aP7Z').get_text()
    price = price.removesuffix('99')
    print(price)

    in_stock = soup.find('span', class_='availabilityMessage_ig-s5 container_1DAvI').get_text()
    print("In Stock:", in_stock)

    return title, price

def is_it_in_stock(avbl: str) -> str:
    if avbl == 'InStock':
        return ("Yes")
    else:
        return ("No")

def dashed_line():
    print('------------------')

def add_to_csv(title: str, date, price: int):
    with open('prices.csv', 'a', newline='' ) as data:
        writer = csv.writer(data)
        writer.writerow([date, title, price])



if __name__ == '__main__':
    json_data = json.load(open('info.json'))
    today_date = date.today()
    print("Date:", today_date)
    dashed_line()
    title_bb, price_bb = bestbuy_price()
    add_to_csv(title_bb, today_date, price_bb)
    dashed_line()
    title_new, price_ne = newegg_price()
    add_to_csv(title_new, today_date, price_ne)
