from pandas_ods_reader import read_ods
import random

ods_path = "./Cities.ods"

with open("./cities.txt", encoding='utf-8') as file:
	cities_title = [row.strip() for row in file]

cities = read_ods(ods_path, 1, headers=True)
cities.index = cities.index + 1


def full_list():
	print('\nСписок доступных городов:')
	for city in cities_title:
		print(city)


def random_city():
	print('\n', cities.iloc[random.randint(0, 30)], '\n')


def find_city(title):
	num_cities = cities.shape[0]
	for i in range(num_cities):
		
		if cities.iloc[i]['Город'].lower() == title.lower():
			print('\n', cities.iloc[i], '\n')
			return
	
	return -1


def output_cities(phrase, selected_attributes):
	count = 0
	num_cities = cities.shape[0]

	for i in range(num_cities):
		if (cities.iloc[i][selected_attributes] and 
			cities.iloc[i][selected_attributes].lower() in set(phrase)):
			count = 1
			print('\n', cities.iloc[i], '\n')
			print('---------------------\n')

	if count == 0:
		print('\nНичего не смогла найти(((')