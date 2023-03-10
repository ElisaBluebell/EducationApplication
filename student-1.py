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
from select import *
from socket import *


FORMAT = 'utf-8'
SERVER = '10.10.21.121'
PORT = 9000
BUFFER = 1024
ADDR = (SERVER, PORT)

form_class = uic.loadUiType("tracking.ui")[0]


class StudentWindow(QMainWindow, form_class):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.sock = socket()
        self.socks = []
        self.connect = True
        self.thread_switch = 0
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

        self.connectserver()

    def connectserver(self):
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.socks.append(self.sock)
        self.sock.connect(ADDR)
        self.thread_switch = 1

        get_message = threading.Thread(target=self.get_message, daemon=True)
        get_message.start()

    def get_message(self):
        while self.connect:
            if self.thread_switch == 1:
                r_sock, dummy1, dummy2 = select(self.socks, [], [], 2)
                if r_sock:
                    for s in r_sock:
                        if s == self.sock:
                            message = eval(self.sock.recv(BUFFER).decode())
                            print(f'받은 메시지 : {message} [{datetime.datetime.now()}]')
                            self.command_processor(message[0], message[1])

    def command_processor(self, command, content):

        if command == '/register_fail':
            print("회원가입이 실패했습니다.(id) 중복")
            self.register_fail()

        elif command == '/register_success':
            print("회원가입이 성공했습니다.")
            self.register_success()

        elif command == '/login_id_fail':
            print("아이디가 존재하지 않아 로그인에 실패 했습니다.")
            self.login_id_fail()

        elif command == '/login_password_fail':
            print("비밀번호가 일치하지 않아 로그인에 실패 했습니다.")
            self.login_password_fail()

        elif command == '/login_success':
            print("로그인에 성공 했습니다.")
            self.login_success()
        else:
            pass

    def login_id_fail(self):
        win32api.MessageBox(0, '로그인에 실패했습니다. ID를 확인 해 주세요.', '로그인실패', 16)

    def login_password_fail(self):
        win32api.MessageBox(0, '로그인에 실패했습니다. 비밀번호를 확인 해 주세요.', '로그인실패', 16)

    def login_success(self):
        win32api.MessageBox(0, '로그인에 성공하였습니다. 환영합니다.', '로그인완료', 0)
        self.tabWidget.setCurrentIndex(1)

    def register_success(self):
        win32api.MessageBox(0, '회원가입이 완료되었습니다. 환영합니다.', '등록완료', 0)
        self.register_name.clear()
        self.register_id.clear()
        self.register_password.clear()

    def register_fail(self):
        win32api.MessageBox(0, 'ID가 중복되었습니다. 다른 아이디를 입력 해 주세요.', '중복알림', 48)

    def quiz_request(self):
        # 버튼 객체 얻기
        btn = self.sender()

        self.quize_name = btn.text()
        if self.quize_name == '서울/경기':
            self.send_command('/quize_seoul', self.quize_name)
        elif self.quize_name == '강원도':
            self.send_command('/quize_gangwon', self.quize_name)
        elif self.quize_name == '충청북도':
            self.send_command('/quize_chungbuk', self.quize_name)
        elif self.quize_name == '충청남도':
            self.send_command('/quize_chungnam', self.quize_name)
        elif self.quize_name == '경상북도':
            self.send_command('/quize_gyeongbuk', self.quize_name)
        elif self.quize_name == '경상남도':
            self.send_command('/quize_gyeongnam', self.quize_name)
        elif self.quize_name == '전라북도':
            self.send_command('/quize_jeonbuk', self.quize_name)
        elif self.quize_name == '전라남도':
            self.send_command('/quize_jeonnam', self.quize_name)
        else:
            self.send_command('/quize_jeju', self.quize_name)

        # 버튼 객체 얻어서 그 버튼이 어떤 도의 버튼인지 확인 후 서버에 데이터 요청해야함

    def send_command(self, command, content):
        msg = [command, content]
        data = json.dumps(msg)
        print(f'보낸 메시지: {data} [{datetime.datetime.now()}]')

        self.sock.send(data.encode())

    def register_server(self):
        self.r_name = self.register_name.text()
        self.r_id = self.register_id.text()
        self.r_password = self.register_password.text()
        self.r_status = self.status_comboBox.currentText()
        self.signuplist = [self.r_status, self.r_name, self.r_id, self.r_password]

        if '' not in self.signuplist:
            print("회원가입시도 : ", self.signuplist)
            self.send_command('/register_student', self.signuplist)
            ###받고  성공-1 실패-0 ###

        else:
            QMessageBox.information(self, '알림', '모든 항목을 입력 해 주세요.')

        pass

    def login(self):
        self.id = self.teacher_id.text()
        self.password = self.teacher_pw.text()
        self.loginlist = [self.id, self.password]
        if '' not in self.loginlist:
            self.send_command('/login_teacher', self.loginlist)
        # self.tabWidget.setCurrentIndex(2)

        else:
            QMessageBox.information(self, '알림', '모든 항목을 입력 해 주세요.')

    # def mainpage(self):
    #     self.tabWidget.setCurrentIndex(0)

    def sign(self):
        self.tabWidget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StudentWindow()
    win.show()
    app.exec_()