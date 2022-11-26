from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QTextEdit
import sys

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

        self.ui.btn_like_1.clicked.connect(self.btn_like1_click)
        self.ui.btn_like_2.clicked.connect(self.btn_like2_click)
        self.ui.btn_like_3.clicked.connect(self.btn_like3_click)
        self.ui.btn_like_4.clicked.connect(self.btn_like4_click)
        self.ui.btn_like_5.clicked.connect(self.btn_like5_click)
        self.ui.btn_like_6.clicked.connect(self.btn_like6_click)

        self.ui.btn_dislike_1.clicked.connect(self.btn_dislike1_click)
        self.ui.btn_dislike_2.clicked.connect(self.btn_dislike2_click)
        self.ui.btn_dislike_3.clicked.connect(self.btn_dislike3_click)
        self.ui.btn_dislike_4.clicked.connect(self.btn_dislike4_click)
        self.ui.btn_dislike_5.clicked.connect(self.btn_dislike5_click)
        self.ui.btn_dislike_6.clicked.connect(self.btn_dislike6_click)

        self.ui.btn_delete_like.clicked.connect(self.btn_delete_like_click)
        self.ui.btn_delete_dislike.clicked.connect(self.btn_delete_dislike_click)


    def btn_like1_click(self):
        city_name = self.ui.name_1.text()
        self.btn_like_click(city_name)

    def btn_like2_click(self):
        city_name = self.ui.name_2.text()
        self.btn_like_click(city_name)
    
    def btn_like3_click(self):
        city_name = self.ui.name_3.text()
        self.btn_like_click(city_name)
    
    def btn_like4_click(self):
        city_name = self.ui.name_4.text()
        self.btn_like_click(city_name)
    
    def btn_like5_click(self):
        city_name = self.ui.name_5.text()
        self.btn_like_click(city_name)
    
    def btn_like6_click(self):
        city_name = self.ui.name_6.text()
        self.btn_like_click(city_name)

    def btn_like_click(self, city_name):
        self.clear_properties()
        
        like_cities, dislike_cities, cities = update_likes(self.user, city_name)
        if (cities):
            self.output_cities(like_cities, dislike_cities, cities)


    def btn_dislike1_click(self):
        city_name = self.ui.name_1.text()
        self.btn_dislike_click(city_name)

    def btn_dislike2_click(self):
        city_name = self.ui.name_2.text()
        self.btn_dislike_click(city_name)
    
    def btn_dislike3_click(self):
        city_name = self.ui.name_3.text()
        self.btn_dislike_click(city_name)
    
    def btn_dislike4_click(self):
        city_name = self.ui.name_4.text()
        self.btn_dislike_click(city_name)
    
    def btn_dislike5_click(self):
        city_name = self.ui.name_5.text()
        self.btn_dislike_click(city_name)
    
    def btn_dislike6_click(self):
        city_name = self.ui.name_6.text()
        self.btn_dislike_click(city_name)

    def btn_dislike_click(self, city_name):
        self.clear_properties()
        
        like_cities, dislike_cities, cities = update_dislikes(self.user, city_name)
        if (cities):
            self.output_cities(like_cities, dislike_cities, cities)


    def btn_delete_like_click(self):
        self.clear_properties()
        
        likes = self.ui.text_like_cities.toPlainText()
        if (len(likes) > 20):
            like_cities, dislike_cities, cities = update_likes(self.user)
            if (cities):
                self.output_cities(like_cities, dislike_cities, cities)


    def btn_delete_dislike_click(self):
        self.clear_properties()
        
        like_cities, dislike_cities, cities = update_dislikes(self.user)
        if (cities):
            self.output_cities(like_cities, dislike_cities, cities)


    def btn_find_click(self):
        self.ui.frame_cities.setVisible(False)
        self.ui.frame_search.setVisible(True)
        self.ui.text_found_cities.setVisible(True)
        self.ui.text_found_cities.clear()

        name = self.ui.line_city_input.text()
        theme = self.ui.combo_theme.currentText()
        in_ring = self.ui.check_in_ring.isChecked()
        out_ring = self.ui.check_out_ring.isChecked()
        distance = self.ui.combo_distance.currentText()

        cities = find_cities_by_filters(name, theme, in_ring, out_ring, distance)
        
        for city in cities:
            self.ui.text_found_cities.append(city.to_string())


    def btn_back_click(self):
        self.ui.frame_cities.setVisible(False)
        self.ui.frame_search.setVisible(False)
        self.ui.frame_login.setVisible(True)
        self.ui.btn_back.setVisible(False)
        
        self.ui.line_name_input.clear()
        self.clear_properties()

        logout(self.user)

    def clear_properties(self):
        self.ui.properties_1.clear()
        self.ui.properties_2.clear()
        self.ui.properties_3.clear()
        self.ui.properties_4.clear()
        self.ui.properties_5.clear()
        self.ui.properties_6.clear()

    def output_city(self, name, properties, city):
        name.setText(city["Город"])
        
        properties.append("Область: " + city["Область"])
        properties.append("Тематика: " + city["Тематика"])
        properties.append("Золотое кольцо: " + city["ЗК"])
        properties.append("Направление: " + city["Направление"])
        properties.append("Расстояние от Москвы: " + str(city["Расстояние от Москвы"]) + " км")
        properties.append("Население: " + city["Население"])


    def output_cities(self, like_cities, dislike_cities, recommend_cities):
        self.ui.text_like_cities.setText("Любимые города:")
        self.ui.text_dislike_cities.setText("Нелюбимые города:")

        for city in like_cities:
            self.ui.text_like_cities.append('  ' + city["Город"])

        for city in dislike_cities:
            self.ui.text_dislike_cities.append('  ' + city["Город"])

        self.output_city(self.ui.name_1, self.ui.properties_1, recommend_cities[0])
        self.output_city(self.ui.name_2, self.ui.properties_2, recommend_cities[1])
        self.output_city(self.ui.name_3, self.ui.properties_3, recommend_cities[2])
        self.output_city(self.ui.name_4, self.ui.properties_4, recommend_cities[3])
        self.output_city(self.ui.name_5, self.ui.properties_5, recommend_cities[4])
        self.output_city(self.ui.name_6, self.ui.properties_6, recommend_cities[5])


    def btn_login_click(self):
        self.user = "Max"
        #self.user = self.ui.line_name_input.text()
        if (self.user):
            self.ui.frame_login.setVisible(False)
            self.ui.frame_search.setVisible(True)
            self.ui.frame_cities.setVisible(True)
            self.ui.btn_back.setVisible(True)
            
            like_cities, dislike_cities, cities = login(self.user)
            self.output_cities(like_cities, dislike_cities, cities)



if __name__ == "__main__":
    app = QApplication([])

    application = mywindow()
    application.show()

    sys.exit(app.exec())
