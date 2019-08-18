from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


class AmRuParser:
    def __init__(self, start_url, total_pages=5):
        self.total_pages = total_pages
        self.driver = webdriver.Chrome('../chromedriver')
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

    def __find_imgs_in_advert(self, href):
        self.driver.get(href)
        links = self.driver.find_elements_by_xpath('//div[@id="page-body"]//div/div/div/figure/picture/img')
        return list(map(lambda x: x.get_attribute('src'), links))

    def get_hrefs(self):
        img_hrefs = []
        for n_page in tqdm(range(self.total_pages)):
            advert_hrefs = self.__find_adverts_on_page()
            next_page_href = self.__find_next_page()
            for advert_href in advert_hrefs:
                img_hrefs += self.__find_imgs_in_advert(advert_href)
            if next_page_href is None:
                break
            self.driver.get(next_page_href)
        return img_hrefs

    def close_driver(self):
        self.driver.close()

if __name__ == '__main__':
    parser = AmRuParser(start_url='https://auto.youla.ru/rossiya/cars/used/?carColors%5B0%5D=16', total_pages=2)
    hrefs = parser.get_hrefs()
