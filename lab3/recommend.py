import os
import itertools
import numpy as np
from tabulate import tabulate

from read_write_data import load_data
from measures import *

limit = 5

def get_measures_for_city(data_fact, like_city_id):
	city = data_fact.iloc[like_city_id]
	measures = []

	num_cities = data_fact.shape[0]
	for i in range(num_cities):
		if (i == like_city_id):
			continue
		cur_city = data_fact.iloc[i]

		measure = Euclidean_measure(city, cur_city)
		measures.append([measure, i])

	measures.sort()
	return measures[:limit]

def matc_data_with_fact_data(data, measures):
	cities = []
	for i in range(len(measures)):
		cur_idx = measures[i][1]
		cities.append(data.iloc[cur_idx])

	return cities


def recommend_by_like(like_city_id):
	data, nodes, data_fact = load_data()
	measures = get_measures_for_city(data_fact, like_city_id)
	
	cities = matc_data_with_fact_data(data, measures)
	cities.insert(0, data.iloc[like_city_id])

	return cities

def recommend_by_array_likes(array_likes):
	
