from pandas_ods_reader import read_ods
from tabulate import tabulate
import pandas as pd
import numpy as np
import json

ods_path = "./Cities.ods"
json_path = "./Nodes.json"
html_path = "./Table.html"
tree_path = "./Tree.json"


def get_data_from_ods(ods_path):
    data = read_ods(ods_path, 1, headers=True)
    data.index = data.index + 1
    return data


def get_data_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data


def write_data_to_json(json_path, json_data):
    with open(json_path, "w") as outfile:
        json.dump(json_data, outfile)


def write_data_to_html(data, html_path):
    f = open(html_path, 'w')
    f.write(tabulate(data, headers="keys", tablefmt='html'))


def factorize_data(data_full, nodes):
    data = data_full.copy(deep=True)

    del data['Город']
    del data['Историческая личность']

    # Факторизация на основе корреляционной матрицы для тематики
    themes = data['Тематика'].str.split(',', 1).str
    data['Тематика'] = themes[0]
    
    themes_list = nodes['Тематика']
    themes_corr = nodes['Тематика.Корреляция']

    for i in range(len(themes_list)):
        data[themes_list[i]] = data['Тематика'].map(lambda e: themes_corr[i][themes_list.index(e)])
    del data['Тематика']

    
    crafts = nodes['Промысел']
    data['Вид промысла'], unique = pd.factorize(data['Вид промысла'], na_sentinel=0)
    data['Вид промысла'] = np.where((data['Вид промысла'] == 0), 0, data['Вид промысла'] / len(crafts))

    #Факторизация списка эпох путем разбиения на 2 списка
    epochs = data['Историческая эпоха'].str.split(',', 1).str
    data['Эпоха1'] = epochs[0]
    data['Эпоха2'] = epochs[1]

    data['Эпоха1'].fillna("", inplace=True)
    data['Эпоха2'].fillna("", inplace=True)

    epochs_list = nodes['Эпоха']
    for epoch in epochs_list:
        data[epoch] = data['Эпоха1'].map(lambda e: 1 if (epoch in e) else 0) + \
                        data['Эпоха2'].map(lambda e: 1 if (epoch in e) else 0)

    del data['Историческая эпоха']
    del data['Эпоха1']
    del data['Эпоха2']


    data['ЗК'], unique = pd.factorize(data['ЗК'])
    data['ЗК'] += 1

    del data['Область']
    del data['Направление']

    data['Расстояние от Москвы'] = data['Расстояние от Москвы'].values / max(data['Расстояние от Москвы'].values)
    
    data['Население'] = [elem.replace('тыс', '') for elem in data['Население']]
    data['Население'] = data['Население'].map(lambda e: float(e))
    data['Население'] = data['Население'].values / max(data['Население'].values)

    return data


def load_data():
    data = get_data_from_ods(ods_path)
    nodes = get_data_from_json(json_path)
    data_fact = factorize_data(data, nodes)

    del data['Историческая личность']

    return data, nodes, data_fact


def get_city_id_by_name(city_name):
	data, nodes, data_fact = load_data()
	idx = -1

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Город'] == city_name:
			idx = i
			break

	return idx


def get_city_by_name(data, name):
	res_city = None

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Город'] == name:
			res_city = cur_city
			break

	return res_city


def get_cities_out_ring(cities):
	res_cities = cities

	if res_cities:
		for city in res_cities:
			if city['ЗК'] == '+':
				res_cities.remove(city)
	else:
		num_cities = data.shape[0]
		for i in range(num_cities):
			cur_city = data.iloc[i]
			if cur_city['ЗК'] == '-':
				res_cities.append(cur_city)

	return res_cities


def get_cities_by_distance(data, cities, distance):
	res_cities = cities
	low_dist, high_dist = 0, 10000

	if distance == 'До 100 км': high_dist = 100
	if distance == '100 - 200': low_dist, high_dist = 100, 200
	if distance == '200 - 500': low_dist, high_dist = 200, 500
	if distance == 'Более 500 км': low_dist = 500

	if res_cities:
		for city in res_cities:
			if city['Расстояние от Москвы'] < low_dist or city['Расстояние от Москвы'] > high_dist:
				res_cities.remove(city)
	else:
		num_cities = data.shape[0]
		for i in range(num_cities):
			cur_city = data.iloc[i]
			if cur_city['Расстояние от Москвы'] > low_dist and cur_city['Расстояние от Москвы'] < high_dist:
				res_cities.append(cur_city)

	return res_cities


def get_cities_by_theme(full_cities, theme):
	res_cities = []

	for city in full_cities:
		if city['Тематика'] == theme:
			res_cities.append(city)

	return res_cities

def get_cities_by_ring(full_cities, ring):
	res_cities = []

	for city in full_cities:
		if city['ЗК'] == ring:
			res_cities.append(city)

	return res_cities


def find_cities_by_filters(name, theme, ring, distance):
	data, nodes, data_fact = load_data()

	num_cities = data.shape[0]
	cities = []

	if name:
		city = get_city_by_name(data, name)
		cities = [city]
		return cities
	
	for i in range(num_cities):
		cities.append(data.iloc[i])
	
	#if theme and theme != 'Тематика':
	#	cities = get_cities_by_theme(cities, theme)

	if ring != None:
		if ring == True:
			cities = get_cities_by_ring(cities, '+')
		if ring == False:
			cities = get_cities_by_ring(cities, '-')

	# if distance != 'Расстояние от Москвы':
	# 	distance_cities = get_cities_by_distance(data, cities, distance)

	return cities


name = None
theme = None
ring = False
distance = None

cities = find_cities_by_filters(name, theme, ring, distance)
print(cities)
print(len(cities))