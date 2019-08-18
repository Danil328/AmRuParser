import os
from multiprocessing.pool import ThreadPool
from itertools import zip_longest
import pandas as pd
from multiprocessing import Pool

from parser import AmRuParser

COLORS = {'black': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=16',
		  'yellow': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=4',
		  'gray': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=13',
		  'silver': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=12',
		  'white': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=2',
		  'blue': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=14',
		  'red': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=8',
		  'brown': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=7',
		  'green': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=5',
		  'light_blue': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=3',
		  'violet': 'https://auto.youla.ru/rossiya/cars/used/?yearMin=2010&carColors%5B0%5D=15',
		  }


def get_hrefs(color):
	parser = AmRuParser(start_url=COLORS[color], total_pages=10)
	hrefs = parser.get_hrefs()
	parser.close_driver()
	return color, hrefs


if __name__ == '__main__':
	results = ThreadPool(processes=8).imap_unordered(get_hrefs, ['black', 'yellow', 'gray', 'silver', 'white', 'blue', 'red', 'brown', 'green'])

	colors = []
	hrefs = []
	for color, href in results:
		hrefs += href
		colors += [color] * len(href)

	df = pd.DataFrame()
	df['color'] = colors
	df['href'] = hrefs
	df.head()

	if not os.path.exists('../output'):
		os.mkdir('../output')
	df.to_csv('../output/colors.csv')