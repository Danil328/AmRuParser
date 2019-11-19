import os
import pandas as pd
from multiprocessing.pool import ThreadPool

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from car import Car
from tqdm import tqdm
from sys import platform

START_PAGES = {'one': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&yearMax=2010&carState=notBroken',
               'two': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2011&yearMax=2011&carState=notBroken',
               'three': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2012&yearMax=2012&carState=notBroken',
               'four': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2013&yearMax=2013&carState=notBroken',
               'five': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2014&yearMax=2014&carState=notBroken',
               'six': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2015&yearMax=2015&carState=notBroken',
               'seven': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2016&yearMax=2016&carState=notBroken',
               'eight': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2017&yearMax=2017&carState=notBroken',
               'nine': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2018&yearMax=2018&carState=notBroken',
               'ten': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2019&yearMax=2019&carState=notBroken',
              }


class AmRuParser:
    def __init__(self, start_url, path_to_driver, total_pages=5):
        self.total_pages = total_pages
        self.driver = webdriver.Chrome(path_to_driver)
        self.page = 1
        self.driver.get(start_url)

    def __find_adverts_on_page(self):
        elems = self.driver.find_elements_by_xpath('//div[@id="serp"]/span/article/div/div/a')
        hrefs = list(map(lambda x: x.get_attribute('href'), elems))
        return hrefs

    def __find_next_page(self):
        self.page += 1
        try:
            next_link = self.driver.find_element_by_xpath(
                f'//*[@id="page-body"]//div/a[@data-target="button-link" and @data-page={self.page}]').get_attribute('href')
        except Exception:
            next_link = None
        return next_link

    def __get_properties_from_advert(self, href):
        self.driver.get(href)
        try:
            images = self.driver.find_elements_by_xpath('//div[@id="page-body"]//div/div/div/figure/picture/img')
            images = list(map(lambda x: x.get_attribute('src'), images))
            brand = self.driver.find_element_by_xpath('//div/div[@data-target="item-breadcrumbs-brand"]/a[@class="blueLink"]').text
            model = self.driver.find_element_by_xpath('//div/div[@data-target="item-breadcrumbs-model"]/a[@class="blueLink"]').text
            generation = self.driver.find_element_by_xpath('//div/div[@data-target="item-breadcrumbs-generation"]/a[@class="blueLink"]').text
            color = self.driver.find_element_by_xpath('//div[@data-target="advert-info-color"]').text
            car = Car(brand=brand, model=model, generation=generation, color=color, images=images).get_object()
        except Exception:
            car = None
        return car

    def parse(self):
        properties = []
        for n_page in tqdm(range(self.total_pages)):
            advert_hrefs = self.__find_adverts_on_page()
            next_page_href = self.__find_next_page()
            for advert_href in advert_hrefs:
                prop = self.__get_properties_from_advert(advert_href)
                if prop is not None:
                    properties += [prop]
            if next_page_href is None:
                break
            self.driver.get(next_page_href)
        return properties

    def close_driver(self):
        self.driver.close()


def get_hrefs(page):
    parser = AmRuParser(start_url=START_PAGES[page], path_to_driver=path_to_driver, total_pages=1)
    properties = parser.parse()
    parser.close_driver()
    return properties


if __name__ == '__main__':

    if platform == "linux" or platform == "linux2":
        path_to_driver = "../cromedriver"
    elif platform == 'darwin':
        path_to_driver = "../chromedriver_mac"

    pages = list(START_PAGES.keys())
    results = ThreadPool(processes=len(pages)).imap_unordered(get_hrefs, pages)

    properties = []
    for p in results:
        properties += p

    brands, models, generations, images = [], [], [], []

    for prop in properties:
        brands.append(prop['brand'])
        models.append(prop['model'])
        generations.append(prop['generation'])
        images.append(prop['images'])

    df = pd.DataFrame()
    df['brand'] = brands
    df['model'] = models
    df['generation'] = generations
    df['url'] = images
    df.head()

    df = df.explode("url")

    if not os.path.exists('../output'):
        os.mkdir('../output')
    df.to_csv('../output/brand_model.csv', index=False)
