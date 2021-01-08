from time import sleep, strftime
from random import randint
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import numpy as np
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.service as service
import smtplib
from email.mime.multipart import MIMEMultipart


class WebScraper:

    def __init__(self, path):
        self.web_browser_path = path
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(executable_path=self.web_browser_path)
        self.action = ActionChains(self.driver)

    def get_web_page(self, url):
        self.driver.get(url)
        sleep(randint(1, 3))

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(randint(1, 3))

    def click_button(self, element):
        self.action.move_to_element(element).perform()
        self.driver.execute_script("arguments[0].click();", element)

    def replace_names(self, name):
        names_mapping = [('ã', 'a'), ('â', 'a'), ('á', 'a'),
                         ('ê', 'e'), ('é', 'e'),
                         ('í', 'i'), ('î', 'i'),
                         ('õ', 'o'), ('ô', 'o'), ('ó', 'o'),
                         ('ú', 'u'), ('û', 'u')]
        for key, value in names_mapping:
            name = name.replace(key, value)
        return name

    def page_scrape(self):
        print('do smth')


class WebMotorsScraper(WebScraper):

    def __init__(self, path, url):
        super(WebMotorsScraper, self).__init__(path)
        self.kayak_web_page = url
        self.get_web_page(url)
        self.manufacturer = ''
        self.model = ''
        self.price_df = None

    def search_used_vehicle(self, city, state, manufacturer, model, year_min, year_max=0):
        self.manufacturer = manufacturer
        self.model = model
        if year_max == 0:
            year_max = datetime.now().year + 1
        city = self.replace_names(city)
        state = self.replace_names(state)
        wm_url = 'https://www.webmotors.com.br/carros/' + str.lower(state) + \
                 '-' + str.lower(city) + '/' + str.lower(manufacturer) + '/' + str.lower(model) + \
                 '/de.' + str(year_min) + '/ate.' + str(year_max)
        self.get_web_page(wm_url)

    def search_new_vehicle(self, manufacturer, model, **filters):
        self.manufacturer = manufacturer
        self.model = model
        wm_url = 'https://www.webmotors.com.br/carros-novos/estoque/' + \
                 str.lower(manufacturer) + '/' + str.lower(model)
        self.get_web_page(wm_url)
        for key in filters.keys():
            self.filter_search(filters[key])
        self.populate_price_list(max_scroll_down=5)

    def filter_search(self, filter_type):
        try:
            element = self.driver.find_element_by_name(filter_type)
            self.click_button(element)
        except:
            print("Element " + filter_type + "not found.")

    def populate_price_list(self, max_scroll_down=5):
        for scroll in range(0, max_scroll_down):
            self.scroll_down()

        time_list = []
        product_list = []
        desc_list = []
        loc_list = []
        price_list = []

        tag_list = self.driver.find_elements_by_tag_name("strong")
        model_list = self.driver.find_elements_by_tag_name("h3")
        location_list = self.driver.find_elements_by_tag_name("span")
        model_dict = self.list_to_dict(model_list)
        location_dict = self.list_to_dict(location_list)

        for item in tag_list:
            text = item.text
            price_text = text.replace("R$ ", "")
            if "R$ " in text:
                pos = (float(item.location['x']), float(item.location['y']))
                model = self.find_by_dist(pos, model_dict)
                location = self.find_by_dist(pos, location_dict)
                price_text = price_text.replace(".", "")
                time_list.append(datetime.now())
                product_list.append(self.manufacturer + "_" + self.model)
                desc_list.append(model)
                loc_list.append(location)
                price_list.append(float(price_text))
        self.price_df = pd.DataFrame([time_list, product_list, desc_list, loc_list, price_list]).transpose()
        self.price_df.columns = ['Time', 'Product', 'Model', 'Location', 'Price']
        print('oi')

    def list_to_dict(self, input_list):
        output_dict = {}
        for item in input_list:
            try:
                output_dict[(float(item.location['x']), float(item.location['y']))] = item.text
            except:
                pass
        return output_dict

    def find_by_dist(self, pos, input_dict):
        x0 = pos[0]
        y0 = pos[1]
        min_dist = 100000
        key_model = 0
        for key in input_dict.keys():
            x1 = key[0]
            y1 = key[1]
            dist = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            value = input_dict[key]
            if dist < min_dist and len(value) != 9:
                key_model = key
                min_dist = dist
        try:
            result = input_dict[key_model]
        except:
            result = 'Não Identificado'
        return result



vehicles_df = pd.DataFrame()
path = './chromedriver.exe'
url = 'https://www.webmotors.com.br/'
wm = WebMotorsScraper(path, url)
filters = {'store_type': 'Concessionária', 'fuel_type': 'Gasolina e álcool', 'category': 'Carros 1.0'}

wm.search_new_vehicle('chevrolet', 'onix', **filters)
vehicles_df = pd.concat([vehicles_df, wm.price_df])
wm.search_new_vehicle('volkswagen', 'gol', **filters)
vehicles_df = pd.concat([vehicles_df, wm.price_df])
wm.search_new_vehicle('hyundai', 'hb20', **filters)
vehicles_df = pd.concat([vehicles_df, wm.price_df])
wm.search_new_vehicle('fiat', 'cronos', **filters)
vehicles_df = pd.concat([vehicles_df, wm.price_df])

vehicles_df.to_csv('veiculos_webmotors.csv')
print(vehicles_df)

