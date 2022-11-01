from recommend import *

# Max liked city Vladimir(id=4)
# Paul liked city Murom(id=16), Vologda(id=5)

def login(user_name):
	if user_name == "Max":
		like_cities, cities = recommend_by_like(4)
	elif user_name == "Paul":
		like_cities, cities = recommend_by_array_likes([5, 16])

	return like_cities, cities