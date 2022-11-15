from read_write_data import load_data

def get_city_by_name(data, name):
	res_city = None

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Город'] == name:
			res_city = cur_city
			break

	return res_city


def get_cities_by_theme(data, theme):
	res_cities = []

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Тематика'] == theme:
			res_cities.append(cur_city)

	return res_cities


def get_cities_in_ring(data, cities):
	res_cities = cities

	if res_cities:
		for city in res_cities:
			if city['ЗК'] == '-':
				res_cities.remove(city)
	else:
		num_cities = data.shape[0]
		for i in range(num_cities):
			cur_city = data.iloc[i]
			if cur_city['ЗК'] == '+':
				res_cities.append(cur_city)

	return res_cities


def get_cities_out_ring(data, cities):
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


def find_cities_by_filters(name, theme, in_ring, out_ring, distance):
	data, nodes, data_fact = load_data()

	cities = []
	if name:
		city = get_city_by_name(data, name)
		cities.append(city)
		return cities
	
	if theme != 'Тематика':
		theme_cities = get_cities_by_theme(data, theme)
		cities = cities + theme_cities

	if in_ring:
		cities = get_cities_in_ring(data, cities)

	if out_ring:
		cities = get_cities_out_ring(data, cities)

	if distance != 'Расстояние от Москвы':
		cities = get_cities_by_distance(data, cities, distance)

	return cities
