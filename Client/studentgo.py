import sys
import socket
import datetime
import json
import select
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
from select import *
from socket import *
import win32api

HEADER = 64  # 기본 메세지 크기 (바이트)
FORMAT = 'utf-8'
SERVER = '10.10.21.121'
PORT = 9000
BUFFER = 8192
ADDR = (SERVER, PORT)

form_class = uic.loadUiType("education.ui")[0]


class MySignal(QtCore.QObject):
    listUser = QtCore.pyqtSignal(str)
    chatLabel = QtCore.pyqtSignal(str)


class StudentWindow(QMainWindow, form_class):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)

        self.BUFFER = 8192
        self.port = 9000
        # 첫번째 로그인 화면 지정
        self.tabWidget.setCurrentIndex(0)

        # 날짜, 시간 사용하기
        self.timer = QTimer(self)  # 윈도우가 생성될 때 QTimer 객체 생성한다.
        self.timer.start(1000)  # 생성한 객체에 interval(1초) 간격 설정
        self.timer.timeout.connect(self.timeout)

        # 스테이터스바 이용하기
        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setValue(50)
        self.statusBar().addPermanentWidget(self.progressbar)
        self.statusBar().setStyleSheet("font: 20px")

        # 서버와 소통하기 위한 소켓 객체 생성 
        self.sock = socket()
        self.socks = []
        self.connect = True
        self.thread_switch = 0

        # 로그인 버튼 클릭시 서버에 데이터 전송
        self.login_btn.clicked.connect(self.login)
        # 회원가입 페이지 이동
        self.signup_btn.clicked.connect(self.sign)
        # 회원가입 중복 체크
        # self.register_confirm_btn.clicked.connect(self.register_confirm_id)
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

        # Q & A 질문하기 버튼 클릭시 발생하는 시그널
        self.ask_btn.clicked.connect(self.ask_question)
        self.ask_check_btn.clicked.connect(self.ask_check)

        # 포인트 조회 버튼
        self.point_check_btn.clicked.connect(self.pointcheck)
        # # 여기는 받는 부분 그런데 항상 받아야 하므로 쓰레드를 생성한다.
        # self.thread_recv = threading.Thread(target=self.recvMsg, args=())
        # self.thread_recv.start()
        self.connectserver()

    def pointcheck(self):
        self.point_label.setText(self.Pointlogin)

    def ask_question(self):
        self.date = f'{self.str_date} / {self.str_time}'
        self.name = '박의용'
        self.ask = self.ask_textEdit.toPlainText()
        self.asklist = [self.date, self.name, self.ask]
        if '' not in self.asklist:
            self.send_command('/ask_student', self.asklist)

    def ask_check(self):
        btn = self.sender()
        check = btn.text()
        self.send_command('/ask_check_student', check)  # "check=질문 조회"

    def timeout(self):
        self.cur_date = QDate.currentDate()
        self.str_date = self.cur_date.toString(Qt.ISODate)
        self.cur_time = QTime.currentTime()
        self.str_time = self.cur_time.toString('hh:mm:ss')
        self.statusBar().showMessage(f'현재 날짜: {self.str_date}, 현재 시간: {self.str_time}')

    def connectserver(self):
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.bufsize = self.sock.getsockopt(SOL_SOCKET, SO_SNDBUF)
        print(self.bufsize)

        # SOL_SOCKET = (프로토콜 레벨. 일반)
        # SO_REUSEADDR = (이미 사용중인 주소나 포트에 대해서도 바인드 허용)
        # 소켓을 이용한 서버프로그램을 운용할 때
        # 강제종료되거나 비정상 종료되는 경우가 발생하는데,
        # 프로그램이 종료되어도 아직 커널이 BIND정보를 유지하고 있음으로
        # 주소가 이미 사용되고 있다고 나온다. 1-2분 정도 가 지나면
        # 이런 오류는 사라지는데 그 시간동안 기다리기 번거로우므로
        # 기존에 BIND로 할당된 소켓자원을 프로세스가 재 사용할 수 있도록 허락한다.
        # 위 프로토콜레벨이나 옵션명은 시스템에서는 정수형 인자로 매핑되어 있다.
        # 즉 시스템에 정의되어 있는 상수 값이다.
        self.socks.append(self.sock)
        self.sock.connect((SERVER, self.port))
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
                            print("hi")
                            message = self.sock.recv(self.BUFFER).decode('unicode_escape')
                            print(type(message))
                            print(message)
                            a = message.split(',')
                            # print(type(a))
                            # print(a)
                            # print(a[0][2:-1])
                            # print('\n',a[1][:-1])
                            # message = list(message)
                            # message = message.split(',')
                            # print(type(message))
                            # print(f'받은 메시지 : {message} [{datetime.datetime.now()}]')
                            # # print(f'\n{fragments[0], fragments[1]}')

                            # # print(f'받은 메시지 : {message} [{datetime.datetime.now()}]')
                            # print(f'\n{message[0], message[1]}')

                            self.command_processor(a[0][2:-1], a)
            else:
                pass

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
            self.login_success(content)

        elif command == '/post_success':
            print('질문 등록에 성공하였습니다.')
            self.post_success()

        elif command == '/whole_qna_data':
            print("질문 조회에 성공하였습니다.")
            self.ask_success(content)

        else:
            pass

    # def ask_success(self, content):
    #     win32api.MessageBox(0,'질문 조회가 완료되었습니다.', '질문조회', 0)
    #     self.askcheck = content
    #     print(self.askcheck)

    def post_success(self):
        win32api.MessageBox(0, '질문 등록이 완료되었습니다.', '질문등록', 0)
        self.ask_textEdit.clear()

    def login_id_fail(self):
        win32api.MessageBox(0, '로그인에 실패했습니다. ID를 확인 해 주세요.', '로그인실패', 16)

    def login_password_fail(self):
        win32api.MessageBox(0, '로그인에 실패했습니다. 비밀번호를 확인 해 주세요.', '로그인실패', 16)

    def login_success(self, content):
        win32api.MessageBox(0, '로그인에 성공하였습니다. 환영합니다.', '로그인완료', 0)
        self.quiz_data = content
        self.inforamtion = [self.quiz_data[3], self.quiz_data[4], self.quiz_data[6][:-2]]  # 이름, 아이디, 포인트
        print(self.inforamtion)
        self.Namelogin = self.inforamtion[0]
        self.Idlogin = self.inforamtion[1]
        self.Pointlogin = self.inforamtion[2]
        self.id_label.setText(self.Idlogin)
        self.name_label.setText(self.Namelogin)

        # self.id_label.setText(#아이디)
        # self.name_label.setText(#이름)
        ### 여기서 이름, 아이디 포인트 확인 후 텍스트박스 고정 ####
        ### 문제 인덱스 확인 후 스택 위젯에 미리 쌓아둔다 ###
        ## 해당 버튼 클릭 시 해당 지역에 맞는 문제만 표시하게끔 제어 할수있다 ###
        ## 그리고 메인화면으로 이동 할수 있게 한다. ###
        self.tabWidget.setCurrentIndex(2)

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
            reply = QMessageBox.question(self, '메시지', '서울/경기 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Seoul_quiz = []
                self.Me = []

            else:
                pass

        elif self.quize_name == '강원도':
            reply = QMessageBox.question(self, '메시지', '강원 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Gangwon_quiz = []
            else:
                pass
            # self.send_command('/quize_gangwon',self.quize_name)
        elif self.quize_name == '충청북도':
            reply = QMessageBox.question(self, '메시지', '충청북도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Chungbuk_quiz = []
            else:
                pass
            # self.send_command('/quize_chungbuk',self.quize_name)
        elif self.quize_name == '충청남도':
            reply = QMessageBox.question(self, '메시지', '충청남도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Chungnam_quiz = []
            else:
                pass
        elif self.quize_name == '경상북도':
            reply = QMessageBox.question(self, '메시지', '경상북도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Gyeongbuk_quiz = []
            else:
                pass
        elif self.quize_name == '경상남도':
            reply = QMessageBox.question(self, '메시지', '경상남도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Gyeongnam_quiz = []
            else:
                pass
        elif self.quize_name == '전라북도':
            reply = QMessageBox.question(self, '메시지', '전라북도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Jeonbuk_quiz = []
            else:
                pass
        elif self.quize_name == '전라남도':
            reply = QMessageBox.question(self, '메시지', '전라남도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Jeonnam_quiz = []
            else:
                pass
        else:
            reply = QMessageBox.question(self, '메시지', '제주 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.Jeju_quiz = []
            else:
                pass
            # self.send_command('/quize_jeju',self.quize_name)

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
        self.signuplist = self.r_status, self.r_name, self.r_id, self.r_password

        if '' not in self.signuplist:
            print("회원가입시도 : ", self.signuplist)
            self.send_command('/register_user', self.signuplist)
            ###받고  성공-1 실패-0 ###

        else:
            QMessageBox.information(self, '알림', '모든 항목을 입력 해 주세요.')

    def login(self):
        self.id = self.student_id.text()
        self.password = self.student_password.text()
        self.loginlist = [self.id, self.password]
        if '' not in self.loginlist:
            self.send_command('/login_student', self.loginlist)
        # self.tabWidget.setCurrentIndex(2)

        else:
            QMessageBox.information(self, '알림', '모든 항목을 입력 해 주세요.')

    def mainpage(self):
        self.tabWidget.setCurrentIndex(0)

    def sign(self):
        self.tabWidget.setCurrentIndex(1)


# class Client():

#     def __init__(self, username, address, port, win):
#         # 연결 유형 정리
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#         ADDR = (address, int(port))
#         self.client.connect(ADDR)

#         self.username = username
#         self.win = win
#         self.online = True

#         # 여기서부터 서버에 보내는 게 시작됨.

#         message, send_length = encodeMsg(self.username)


# def encodeMsg(msg):

#     message = str(msg).encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))

#     return message, send_length

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StudentWindow()
    win.show()
    app.exec_()
