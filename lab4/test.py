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
			if city['Расстояние от Москвы'] < low_dist || city['Расстояние от Москвы'] > high_dist:
				res_cities.remove(city)
	else:
		num_cities = data.shape[0]
		for i in range(num_cities):
			cur_city = data.iloc[i]
			if city['Расстояние от Москвы'] > low_dist && city['Расстояние от Москвы'] < high_dist:
				res_cities.append(cur_city)

	return res_cities


data, nodes, data_fact = load_data()

cities = get_cities_by_theme(data, "Гастрономия")
cities_ring = get_cities_in_ring(data, [])

print(cities)
print('----------')
print(cities_ring)
