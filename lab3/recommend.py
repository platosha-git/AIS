import os
import itertools
import numpy as np
import pandas as pd
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

		measure = Minkowski_measure(0.5, city, cur_city)
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
	like_city = data.iloc[like_city_id]

	return [like_city], cities


def recommend_by_array_likes(array_likes):
	data, nodes, data_fact = load_data()
	matrix = get_correlation_matix(data_fact, Minkowski_measure)
	
	measures = []
	for like in array_likes:
		cur_measures = get_measures_for_city(data_fact, like)

		if (not measures):
			measures = cur_measures
		else:
			for i in range(len(measures)):
				measures[i] = measures[i] if measures[i][0] < cur_measures[i][0] else cur_measures[i]

	cities = matc_data_with_fact_data(data, measures)
	
	like_cities = []
	for like in array_likes:
		like_city = data.iloc[like]
		like_cities.append(like_city)

	return like_cities, cities

