from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
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

    def get_web_page(self, url):
        self.driver.get(url)
        sleep(randint(5,10))

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

    def start_wm(self, city, state, manufacturer, model):
        city = self.replace_names(city)
        state = self.replace_names(state)
        wm_url = 'https://www.webmotors.com.br/carros/' + str.lower(state) + \
                 '-' + str.lower(city) + '/' + str.lower(manufacturer) + '/' + str.lower(model)
        self.get_web_page(wm_url)


path = 'C:/Users/Gustavo/Desktop/chromedriver.exe'
url = 'https://www.webmotors.com.br/'
wm = WebMotorsScraper(path, url)
wm.start_wm('São Paulo', 'Sp', 'Volkswagen', 'gol')