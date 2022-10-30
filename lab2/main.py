import os
import itertools
import numpy as np
import pandas as pd
from tabulate import tabulate

from read_write_data import *
from measures import *


ods_path = "./Cities.ods"
json_path = "./Nodes.json"
html_path = "./Table.html"

def factorize_data(data, nodes):
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


def main():
	os.system("clear")

	data = get_data_from_ods(ods_path)
	nodes = get_data_from_json(json_path)
	#print(tabulate(data, headers="keys"))
	#print('\n')

	data_fact = factorize_data(data, nodes)
	write_data_to_html(data_fact, html_path)
	#print(tabulate(data_fact, headers="keys"))

	matrix1 = get_correlation_matix(data_fact, Euclidean_measure)
	matrix2 = get_correlation_matix(data_fact, City_block_distance)
	matrix3 = get_correlation_matix(data_fact, Cosine_measure)
	matrix4 = get_correlation_matix(data_fact, Chebyshev_measure)

	plot_matrices(matrix1, 'Евклидово расстояние', \
					matrix2, 'Расстояние городских кварталов', \
					matrix3, 'Косинусная мера', \
					matrix4, 'Расстояние Чебышева')


if __name__ == "__main__":
	main()
