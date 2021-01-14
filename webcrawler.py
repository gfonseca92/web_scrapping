from crawlerlib import WebMotorsScraper, MagaluScrapper
import pandas as pd

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


electronics_df = pd.DataFrame()
path = './chromedriver.exe'
url = 'https://www.magazineluiza.com.br/'
ml = MagaluScrapper(path, url)

filters = {'product_type': 'tvs'}
ml.search_electronic('tv 32"', **filters)
electronics_df = pd.concat([electronics_df, ml.price_df])

filters = {'product_type': 'máquina de lavar'}
ml.search_electronic('máquina de lavar', **filters)
electronics_df = pd.concat([electronics_df, ml.price_df])

filters = {'product_type': 'micro-ondas'}
ml.search_electronic('micro-ondas', **filters)
electronics_df = pd.concat([electronics_df, ml.price_df])

filters = {'product_type': 'geladeira'}
ml.search_electronic('geladeira', **filters)
electronics_df = pd.concat([electronics_df, ml.price_df])

electronics_df.to_csv('eletronicos.csv')
print(electronics_df)