from read_write_data import load_data

def get_cities_by_theme(data, theme):
	res_cities = []

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Тематика'] == theme:
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
			if city['Расстояние от Москвы'] > low_dist and city['Расстояние от Москвы'] < high_dist:
				res_cities.append(cur_city)

	return res_cities


# data, nodes, data_fact = load_data()

# cities = get_cities_by_theme(data, "Гастрономия")
# cities_ring = get_cities_in_ring(data, [])

# print(cities)
# print('----------')
# print(cities_ring)

def get_city_id_by_name(city_name):
	data, nodes, data_fact = load_data()
	cities = data['Город']

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Город'] == city_name:
			print(i)
			break

	#for city in data:
	#	print(city)
	
	'''
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
	'''


#id_city = get_city_id_by_name("Суздаль")