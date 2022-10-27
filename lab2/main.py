import os
import numpy as np
import pandas as pd
from tabulate import tabulate
from read_data import *

ods_path = "./Cities.ods"
json_path = "./Nodes.json"

def factorize_data(data, nodes):
	del data['Город']
	del data['Историческая личность']


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


	#epochs = nodes['Эпоха']

	
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
	print(tabulate(data_fact, headers="keys"))


if __name__ == "__main__":
	main()
