from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QTextEdit, QScrollArea
import sys
import math
from functools import partial

from forms import *
from authorization import *
from filter import find_cities_by_filters


class mywindow(QMainWindow):
	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.user = ""

		self.ui.frame_login.setVisible(True)
		self.ui.frame_cities.setVisible(False)
		self.ui.frame_search.setVisible(False)
		self.ui.btn_back.setVisible(False)

		self.ui.btn_login.clicked.connect(self.btn_login_click)
		self.ui.btn_back.clicked.connect(self.btn_back_click)
		self.ui.btn_find.clicked.connect(self.btn_find_click)

		self.frame_cities = [self.ui.frame_city_1, self.ui.frame_city_2, self.ui.frame_city_3, \
							self.ui.frame_city_4, self.ui.frame_city_5, self.ui.frame_city_6]
		self.city_names = [self.ui.name_1, self.ui.name_2, self.ui.name_3, \
							self.ui.name_4, self.ui.name_5, self.ui.name_6]
		self.properties = [self.ui.properties_1, self.ui.properties_2, self.ui.properties_3, \
							self.ui.properties_4, self.ui.properties_5, self.ui.properties_6]

		self.btns_like = [self.ui.btn_like_1, self.ui.btn_like_2, self.ui.btn_like_3, \
							self.ui.btn_like_4, self.ui.btn_like_5, self.ui.btn_like_6]
		self.btns_dislike = [self.ui.btn_dislike_1, self.ui.btn_dislike_2, self.ui.btn_dislike_3, \
							self.ui.btn_dislike_4, self.ui.btn_dislike_5, self.ui.btn_dislike_6]
		

		self.connect_like_click()
		self.connect_dislike_click()


		self.ui.btn_delete_like.clicked.connect(self.btn_delete_like_click)
		self.ui.btn_delete_dislike.clicked.connect(self.btn_delete_dislike_click)


	def connect_like_click(self, filter_mode=False):
		for i in range(len(self.btns_like)):
			city_name = self.city_names[i]

			if filter_mode:
				self.btns_like[i].clicked.connect(partial(self.btn_like_filters_click, city_name))
			else:
				self.btns_like[i].clicked.connect(partial(self.btn_like_click, city_name))


	def btn_like_click(self, city_name):
		self.clear_properties()
		city_name = city_name.text()
		
		like_cities, dislike_cities, cities = update_likes(self.user, city_name)
		if (cities):
			self.output_recommend_cities(like_cities, dislike_cities, cities)

	def btn_like_filters_click(self, city_name):
		city_name = city_name.text()		
		like_cities, dislike_cities, cities = update_likes(self.user, city_name)

		self.output_header_likes_dislikes(like_cities, dislike_cities)


	def connect_dislike_click(self, filter_mode=False):
		for i in range(len(self.btns_dislike)):
			city_name = self.city_names[i]

			if filter_mode:
				self.btns_dislike[i].clicked.connect(partial(self.btn_dislike_filters_click, city_name))
			else:
				self.btns_dislike[i].clicked.connect(partial(self.btn_dislike_click, city_name))


	def btn_dislike_click(self, city_name):
		self.clear_properties()
		city_name = city_name.text()

		like_cities, dislike_cities, cities = update_dislikes(self.user, city_name)
		if (cities):
			self.output_recommend_cities(like_cities, dislike_cities, cities)

	def btn_dislike_filters_click(self, city_name):
		city_name = city_name.text()		
		like_cities, dislike_cities, cities = update_dislikes(self.user, city_name)

		self.output_header_likes_dislikes(like_cities, dislike_cities)


	def btn_delete_like_click(self):
		self.clear_properties()
		
		likes = self.ui.text_like_cities.toPlainText()
		if (len(likes) > 20):
			like_cities, dislike_cities, cities = update_likes(self.user)
			if (cities):
				self.output_recommend_cities(like_cities, dislike_cities, cities)

	def btn_delete_dislike_click(self):
		self.clear_properties()
		
		like_cities, dislike_cities, cities = update_dislikes(self.user)
		if (cities):
			self.output_recommend_cities(like_cities, dislike_cities, cities)


	def btn_find_click(self):
		self.clear_frames()

		name = self.ui.line_city_input.text()
		theme = self.ui.combo_theme.currentText()
		in_ring = self.ui.check_in_ring.isChecked()
		out_ring = self.ui.check_out_ring.isChecked()
		distance = self.ui.combo_distance.currentText()

		cities = find_cities_by_filters(name, theme, in_ring, out_ring, distance)

		for i in range(len(cities)):
			frame_city, name, properties, btn_like, btn_dislike = \
				add_frame(self.ui.scrollAreaWidgetContents, i)   
			self.ui.gridLayout.addWidget(frame_city, math.floor((i+3) / 3), i % 3, 1, 1)   

			self.frame_cities.append(frame_city)
			self.city_names.append(name)
			self.properties.append(properties)
			self.btns_like.append(btn_like)
			self.btns_dislike.append(btn_dislike)

		if cities:
			self.connect_like_click(filter_mode=True)
			self.connect_dislike_click(filter_mode=True)
			self.output_cities(cities)


	def clear_frames(self):
		for i in range(len(self.frame_cities)):
		# if (len(self.frame_cities) > 6):
		# 	self.ui.gridLayout.removeWidget(self.ui.frame_city_1)
		# 	self.ui.frame_city_1.deleteLater()
		# 	del self.ui.frame_city_1
			self.frame_cities[i].hide()


		del self.frame_cities[0:]
		del self.city_names[0:]
		del self.properties[0:]
		del self.btns_like[0:]
		del self.btns_dislike[0:]


	def btn_back_click(self):
		self.ui.frame_cities.setVisible(False)
		self.ui.frame_search.setVisible(False)
		self.ui.frame_login.setVisible(True)
		self.ui.btn_back.setVisible(False)
		
		self.ui.line_name_input.clear()
		self.clear_properties()

		logout(self.user)


	def clear_properties(self):
		for cur_property in self.properties:
			cur_property.clear()


	def output_city(self, name, properties, city):
		name.setText(city["Город"])
		
		properties.append("Область: " + city["Область"])
		properties.append("Тематика: " + city["Тематика"])
		properties.append("Золотое кольцо: " + city["ЗК"])
		properties.append("Направление: " + city["Направление"])
		properties.append("Расстояние от Москвы: " + str(city["Расстояние от Москвы"]) + " км")
		properties.append("Население: " + city["Население"])


	def output_recommend_cities(self, like_cities, dislike_cities, recommend_cities):
		self.output_header_likes_dislikes(like_cities, dislike_cities)
		self.output_cities(recommend_cities)


	def output_header_likes_dislikes(self, like_cities, dislike_cities):
		self.ui.text_like_cities.setText("Любимые города:")
		self.ui.text_dislike_cities.setText("Нелюбимые города:")

		for city in like_cities:
			self.ui.text_like_cities.append('  ' + city["Город"])

		for city in dislike_cities:
			self.ui.text_dislike_cities.append('  ' + city["Город"])


	def output_cities(self, cities):
		min_len = min(len(cities), len(self.city_names))
		for i in range(min_len):
			cur_name = self.city_names[i]
			cur_property = self.properties[i]
			cur_city = cities[i]
			self.output_city(cur_name, cur_property, cur_city)


	def btn_login_click(self):
		self.user = "Max"
		#self.user = self.ui.line_name_input.text()
		if (self.user):
			self.ui.frame_login.setVisible(False)
			self.ui.frame_search.setVisible(True)
			self.ui.frame_cities.setVisible(True)
			self.ui.btn_back.setVisible(True)
			
			like_cities, dislike_cities, cities = login(self.user)
			self.output_recommend_cities(like_cities, dislike_cities, cities)



if __name__ == "__main__":
	app = QApplication([])

	application = mywindow()
	application.show()

	sys.exit(app.exec())
