from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QTextEdit
import sys

from authorization import login

BACKGROUND_PATH = '/home/platosha/Desktop/BMSTU/1Msem/AIS/lab3.1/background.png'

class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.frame_cities.setVisible(False)
        self.ui.btn_back.setVisible(False)

        self.ui.btn_name_input.clicked.connect(self.btn_name_click)
        self.ui.btn_back.clicked.connect(self.btn_back_click)


    def btn_back_click(self):
        self.ui.frame_cities.setVisible(False)
        self.ui.frame_login.setVisible(True)
        self.ui.btn_back.setVisible(False)
        self.ui.line_name_input.clear()


    def output_cities(self, like_cities, dislike_cities, cities):
        self.ui.frame_login.setVisible(False)
        self.ui.frame_cities.setVisible(True)
        self.ui.btn_back.setVisible(True)

        for city in like_cities:
            self.ui.text_like_cities.append(city["Город"])

        for city in dislike_cities:
            self.ui.text_dislike_cities.append(city["Город"])



        city = cities[0].astype("string")
        print(city)
        #self.ui.textEdit.setText(city)


    def btn_name_click(self):
        #user = self.ui.line_name_input.text()
        user = "Sam"
        like_cities, dislike_cities, cities = login(user)
        if (cities):
            self.output_cities(like_cities, dislike_cities, cities)



if __name__ == "__main__":
    app = QApplication([])

    application = mywindow()
    application.show()

    sys.exit(app.exec())
