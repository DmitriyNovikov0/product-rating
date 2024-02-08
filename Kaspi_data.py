import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from os import path
import sys
import datetime
import re
import csv

class Kaspi_data:
    FILENAME = "product.csv"
    product_list = []

    def __init__(self, url_site = 'https://kaspi.kz/shop/search/?text=xiaomi&sort=relevance', product = '', browser = 'firefox', test = False, hideBrouser = True):
        self.__url = url_site
        self.product = product
        self.__current_date = datetime.datetime.now().strftime("%Y.%m.%d")
        parent_dir = path.dirname(path.abspath(__file__))
        if test:
            return
        if browser == 'firefox':
            #поднастроим firfox :) - скроем автоматизацию
            option = webdriver.FirefoxOptions()
            option.set_preference('dom.webdriver.enabled', False)
            option.set_preference('dom.webnotification.enabled', False)
            option.headless = hideBrouser
            option.set_preference('general.useragent.override', 'hello :)')
            #проверим разрядность ОС
            if sys.maxsize > 2**32:
                self.__browser = webdriver.Firefox(executable_path = parent_dir + '\\drivers\\geckodriver_x64.exe', options=option)
            else:
                self.__browser = webdriver.Firefox(executable_path = parent_dir + '\\drivers\\geckodriver_x86.exe', options=option)
        else:
            self.__browser = webdriver.Chrome(executable_path = parent_dir + '\\drivers\\chromedriver.exe')

    def __open_page_site(self, page_nmb = 1):
        try:
            self.__browser.get(self.__url + '?text=' + self.product +  '&sort=relevance&page=' + str(page_nmb))
            return True
        except:
            pass
            #print(f'Ошибка открытия сайта {self.__url}' )

    def products_analiysis(self, product):
        result = {
                  'product_id': product.get('data-product-id'),
                  'product_name': product.find('a', class_='item-card__name-link').get_text(strip=True),
                  'product_href': product.find('a', class_='item-card__name-link').get('href'),
                  'price': re.sub(r'[^0-9.]+', r'', product.find('span', class_='item-card__prices-price').get_text(strip=True)),
                  'date': self.__current_date,
                  }

        raiting = product.find('div', class_ = 'item-card__rating')
        if raiting.find('a') is None :
            result['nmb_reviews'] = 0
        else:
            result['nmb_reviews'] = re.sub(r'[^0-9.]+', r'', raiting.find('a').get_text(strip=True))
        result['raiting'] = re.sub(r'[^0-9.]+', r'', raiting.find('span').get('class')[2])

        return result


    def get_date(self, start_page = 1, end_page = 1):
        max_page = 1
        print('Начинаем парсить :)')
        print('определяем максимальное количество страниц для товара....')

        if not self.__open_page_site(1):
            print('Ошибка открытия сайта!')
            exit(0)
        else:
            soup = BeautifulSoup(self.__browser.page_source, 'html.parser')
            parse_data = soup.find('span', class_='search-result__title-count').get_text(strip=True)
            num_list = re.findall(r'\d+', parse_data)
            if num_list[0].isnumeric():
                max_page = int(num_list[0])
            # if int(end_page) < 1 or int(end_page) > max_page or (not end_page.isnumeric()):
            #     end_page = max_page

            for page_nmb in range(start_page, end_page):
                if not self.__open_page_site(page_nmb):
                    print('Ошибка открытия сайта!')
                    exit(0)
                else:
                    soup = BeautifulSoup(self.__browser.page_source, 'html.parser')
                    product_discription_list = soup.findAll('div', class_ = 'item-card ddl_product ddl_product_link undefined')
                    for product_discription in product_discription_list:
                        self.product_list.append(self.products_analiysis(product_discription))
                time.sleep(60)
                print(f'Спарсили страничку № {page_nmb} из {end_page}')
        self.__browser.close()
        self.__browser.quit()


    def saving_data(self, out_format = 'csv'):
        test_date = []

        columns = [
               'product_id', 'product_name', 'product_href', 'price', 'nmb_reviews', 'raiting', 'date'
        ]
        with open(self.FILENAME, "a+", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columns, delimiter=";")
            writer.writeheader()
            writer.writerows(self.product_list)


# [{'product_id': '107221005', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-note-10-pro-8-gb-256-gb-seryi-107221005/?c=750000000', 'product_name': 'Xiaomi Redmi Note 10 Pro 8 ГБ/256 ГБ серый', 'price': '128255', 'nmb_reviews': '150', 'raiting': '10'}, {'product_id': '104417231', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-10c-4-gb-128-gb-seryi-104417231/?c=750000000', 'product_name': 'Xiaomi Redmi 10C 4 ГБ/128 ГБ серый', 'price': '68146', 'nmb_reviews': '548', 'raiting': '10'}, {'product_id': '103971386', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-note-11-pro-8-gb-128-gb-seryi-103971386/?c=750000000', 'product_name': 'Xiaomi Redmi Note 11 Pro 8 ГБ/128 ГБ серый', 'price': '138600', 'nmb_reviews': '599', 'raiting': '10'}, {'product_id': '103541773', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-note-11-4-gb-128-gb-seryi-103541773/?c=750000000', 'product_name': 'Xiaomi Redmi Note 11 4 ГБ/128 ГБ серый', 'price': '99331', 'nmb_reviews': '1015', 'raiting': '10'}, {'product_id': '104417308', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-10c-4-gb-128-gb-goluboi-104417308/?c=750000000', 'product_name': 'Xiaomi Redmi 10C 4 ГБ/128 ГБ голубой', 'price': '69203', 'nmb_reviews': '290', 'raiting': '10'}, {'product_id': '104443164', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-10c-4-gb-128-gb-zelenyi-104443164/?c=750000000', 'product_name': 'Xiaomi Redmi 10C 4 ГБ/128 ГБ зеленый', 'price': '69433', 'nmb_reviews': '193', 'raiting': '10'}, {'product_id': '100399600', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-9a-2-gb-32-gb-seryi-100399600/?c=750000000', 'product_name': 'Xiaomi Redmi 9A 2 ГБ/32 ГБ серый', 'price': '34946', 'nmb_reviews': '2291', 'raiting': '9'}, {'product_id': '104292774', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-note-11s-8-gb-128-gb-seryi-104292774/?c=750000000', 'product_name': 'Xiaomi Redmi Note 11S 8 ГБ/128 ГБ серый', 'price': '112660', 'nmb_reviews': '105', 'raiting': '10'}, {'product_id': '105711712', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-10a-3-gb-64-gb-seryi-grafit-105711712/?c=750000000', 'product_name': 'Xiaomi Redmi 10A 3 ГБ/64 ГБ серый графит', 'price': '54869', 'nmb_reviews': '77', 'raiting': '10'}, {'product_id': '104154272', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-note-11s-6-gb-128-gb-seryi-104154272/?c=750000000', 'product_name': 'Xiaomi Redmi Note 11S 6 ГБ/128 ГБ серый', 'price': '109748', 'nmb_reviews': '219', 'raiting': '10'}, {'product_id': '104417151', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-10c-4-gb-64-gb-seryi-104417151/?c=750000000', 'product_name': 'Xiaomi Redmi 10C 4 ГБ/64 ГБ серый', 'price': '63133', 'nmb_reviews': '155', 'raiting': '10'}, {'product_id': '105202550', 'date': '2023.03.06', 'product_href': 'https://kaspi.kz/shop/p/xiaomi-redmi-9a-2-gb-32-gb-glacial-blue-goluboi-105202550/?c=750000000', 'product_name': 'Xiaomi Redmi 9A 2 ГБ/32 ГБ Glacial Blue голубой', 'price': '34939', 'nmb_reviews': '124', 'raiting': '9'}]
