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
import faulthandler
import time

FORMAT = 'utf-8'
SERVER = '10.10.21.121'
PORT = 9000
BUFFER = 1024
ADDR = (SERVER, PORT)


form_class = uic.loadUiType("education.ui")[0]

class StudentWindow(QMainWindow, form_class):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)

        # 로그인 버튼 클릭시 서버에 데이터 전송
        self.login_btn.clicked.connect(self.login)
        # 회원가입 페이지 이동
        self.signup_btn.clicked.connect(self.sign)
        # 회원가입 버튼 클릭시 서버에 데이터 전송
        self.register_signup_btn.clicked.connect(self.register_server)
        # 로그인 페이지 이동
        self.login_move_btn.clicked.connect(self.mainpage)


        #### 문제풀이에 관한 데이터 요청 버튼 <도별> ####
        self.seoul_btn.clicked.connect(self.quiz_request)
        self.gangwondo_btn.clicked.connect(self.quiz_request)
        self.chungbuk_btn.clicked.connect(self.quiz_request)
        self.chungnam_btn.clicked.connect(self.quiz_request)
        self.gyeongbuk_btn.clicked.connect(self.quiz_request)
        self.gyeongnam_btn.clicked.connect(self.quiz_request)
        self.jeonbuk_btn.clicked.connect(self.quiz_request)
        self.jeonnam_btn.clicked.connect(self.quiz_request)
        self.jeju_btn.clicked.connect(self.quiz_request)

    def quiz_request(self):
        # 버튼 객체 얻기
        btn = self.sender()
        # 버튼 객체 얻어서 그 버튼이 어떤 도의 버튼인지 확인 후 서버에 데이터 요청해야함

    def send_command(self, command, content:list):
        print(command)
        print(content)
        data = json.dumps([command,content])
        print(f'보낸 메시지: {data} [{datetime.datetime.now()}]')

    def register_server(self):
        self.r_name = self.register_name.text()
        self.r_id = self.register_id.text()
        self.r_password = self.register_password.text()
        self.r_status = self.status_comboBox.currentText()
        self.signuplist = [self.r_name, self.r_id, self.r_password, self.r_status]
        print(self.signuplist)
        if '' not in self.signuplist:
            print("회원가입시도 : ", self.signuplist)
            self.send_command('/register_student', self.signuplist)
            self.register_name.clear()
            self.register_id.clear()
            self.register_password.clear()
        else:
            QMessageBox.information(self,'알림', '모든 항목을 입력 해 주세요.')

        pass


    def login(self):
        self.id = self.student_id.text()
        self.password = self.student_password.text()
        self.loginlist = [self.id, self.password]
        print(self.loginlist)
        self.send_command('/login_student', self.loginlist)
        # self.tabWidget.setCurrentIndex(2)

    def mainpage(self):
        self.tabWidget.setCurrentIndex(0)

    def sign(self):
        self.tabWidget.setCurrentIndex(1)
        

#     def sendtoserver(self, username, id, password, address, port):
        
#         self.student = Student(username, id, password, address, port)


# class Student():

#     def __init__(self, username, id, password, address, port):

#         self.student = socket.socket(socket.AF)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StudentWindow()
    win.show()
    app.exec_()