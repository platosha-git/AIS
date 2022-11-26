from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QTextEdit
import sys

from authorization import login
from filter import find_cities_by_filters

BACKGROUND_PATH = '/home/platosha/Desktop/BMSTU/1Msem/AIS/lab3.1/background.png'

class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.frame_login.setVisible(True)
        self.ui.frame_cities.setVisible(False)
        self.ui.frame_search.setVisible(False)
        self.ui.text_found_cities.setVisible(False)
        self.ui.btn_back.setVisible(False)

        self.ui.btn_login.clicked.connect(self.btn_login_click)
        self.ui.btn_back.clicked.connect(self.btn_back_click)
        self.ui.btn_find.clicked.connect(self.btn_find_click)


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
        self.ui.text_found_cities.setVisible(False)
        self.ui.frame_login.setVisible(True)
        self.ui.btn_back.setVisible(False)
        
        self.ui.line_name_input.clear()
        self.ui.text_like_cities.clear()
        self.ui.text_dislike_cities.clear()

        self.ui.text_like_cities.setText("Любимые города:")
        self.ui.text_dislike_cities.setText("Нелюбимые города:")

        self.ui.tableWidget.clear()
        self.ui.text_found_cities.clear()


    def init_table(self):
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setRowCount(8)
        item = QtWidgets.QTableWidgetItem("Город")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.ui.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem("Область")
        self.ui.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem("Тематика")
        self.ui.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem("Историческая эпоха")
        self.ui.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem("ЗК")
        self.ui.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem("Направление")
        self.ui.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem("Расстояние от Москвы")
        self.ui.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem("Население")
        self.ui.tableWidget.setVerticalHeaderItem(7, item)

        item = QtWidgets.QTableWidgetItem("1")
        self.ui.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem("2")
        self.ui.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem("3")
        self.ui.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem("4")
        self.ui.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem("5")
        self.ui.tableWidget.setHorizontalHeaderItem(4, item)

    def output_cities(self, like_cities, dislike_cities, recommend_cities):
        self.ui.text_like_cities.setText("Любимые города:")
        self.ui.text_dislike_cities.setText("Нелюбимые города:")

        for city in like_cities:
            self.ui.text_like_cities.append('  ' + city["Город"])

        for city in dislike_cities:
            self.ui.text_dislike_cities.append('  ' + city["Город"])
        
        self.init_table()

        i = 0
        for city in recommend_cities:
            city_name = city["Город"]
            city_region = city["Область"]
            city_theme = city["Тематика"]
            city_epoch = city["Историческая эпоха"]
            city_ring = city["ЗК"]
            city_direct = city["Направление"]
            city_dist = city["Расстояние от Москвы"]
            city_people = city["Население"]

            name = QtWidgets.QTableWidgetItem(city_name)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            name.setFont(font)
            
            self.ui.tableWidget.setItem(0, i, QTableWidgetItem(name))
            self.ui.tableWidget.setItem(1, i, QTableWidgetItem(city_region))
            self.ui.tableWidget.setItem(2, i, QTableWidgetItem(city_theme))
            self.ui.tableWidget.setItem(3, i, QTableWidgetItem(city_epoch))
            self.ui.tableWidget.setItem(4, i, QTableWidgetItem(city_ring))
            self.ui.tableWidget.setItem(5, i, QTableWidgetItem(city_direct))
            self.ui.tableWidget.setItem(6, i, QTableWidgetItem(str(city_dist)))
            self.ui.tableWidget.setItem(7, i, QTableWidgetItem(city_people))
            i = i + 1


    def btn_login_click(self):
        self.ui.frame_login.setVisible(False)
        self.ui.frame_search.setVisible(True)
        self.ui.frame_cities.setVisible(True)
        self.ui.btn_back.setVisible(True)

        user = self.ui.line_name_input.text()
        #user = "Max"
        like_cities, dislike_cities, cities = login(user)
        
        if (cities):
            self.output_cities(like_cities, dislike_cities, cities)



if __name__ == "__main__":
    app = QApplication([])

    application = mywindow()
    application.show()

    sys.exit(app.exec())
