import sys
import socket
import datetime
import json
import select
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading

FORMAT = 'utf-8'
SERVER = '10.10.21.121'
PORT = 9000
ADDR = (SERVER, PORT)

form_class = uic.loadUiType("education.ui")[0]

class StudentWindow(QMainWindow, form_class):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)

        self.login_btn.clicked.connect(self.mainpage)

        self.signup_btn.clicked.connect(self.sign)

        self.register_signup_btn.clicked.connect(self.register_server)

        self.login_move_btn.clicked.connect(self.login)

    def register_server(self):
        self.name = self.register_name.text()
        self.id = self.register_id.text()
        self.password = self.register_password.text()
        self.status = self.status_comboBox.currentText()

        pass

    def login(self):
        self.tabWidget.setCurrentIndex(0)

    def mainpage(self):
        self.tabWidget.setCurrentIndex(2)
    
    def sign(self):
        self.tabWidget.setCurrentIndex(1)
        

    def sendtoserver(self, username, id, password, address, port):
        
        self.student = Student(username, id, password, address, port)


class Student():

    def __init__(self, username, id, password, address, port):

        self.student = socket.socket(socket.AF)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StudentWindow()
    win.show()
    app.exec_()