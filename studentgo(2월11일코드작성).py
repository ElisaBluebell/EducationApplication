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
import time
import random

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

        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.actionlogout.triggered.connect(self.logout)
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

        #### 문제풀이 시작과 관련된 모든 버튼 및 시그널 #######
        # self.start_learning_btn.clicked.connect()

        # Q & A 질문하기 버튼 클릭시 발생하는 시그널
        self.ask_page_btn.clicked.connect(self.ask_page)
        self.ask_btn.clicked.connect(self.ask_question)
        self.ask_check_btn.clicked.connect(self.ask_check)
        self.ask_board_btn.clicked.connect(self.ask_board)
        # 포인트 조회 버튼
        self.point_check_btn.clicked.connect(self.pointcheck)
        # 상담요청 버튼
        self.consulting_btn.clicked.connect(self.consulting_page)

        # 문제풀이 정답제출 전 o,x체크 확인 하는 시그널
        self.Quiz_answer_groupBox = QButtonGroup()
        self.Quiz_answer_groupBox.addButton(self.radioButton_O)
        self.Quiz_answer_groupBox.addButton(self.radioButton_X)
        self.Quiz_answer_groupBox.buttonPressed.connect(self.quiz_solving)
        self.main_move_btn.clicked.connect(self.main_go)
        self.main_go_btn.clicked.connect(self.main_go)
        self.main_go_btn2.clicked.connect(self.main_go)
        self.main_go_btn3.clicked.connect(self.main_go)

        # 문제풀이 정답 제출하는 시그널
        self.quiz_submit_btn.clicked.connect(self.quiz_submit)
        
        # 학습단계 서버에 전송하는 시그널
        self.save_learning_stage_btn.clicked.connect(self.learning_submit)

        # 다음 문제 푸는 시그널
        self.next_quiz_btn.clicked.connect(self.nextstep)

        # 지역 퀴즈 다풀고 학습완료로 서버에 전송하는 시그널
        self.quiz_finish_btn.clicked.connect(self.laststep)

        # 지난 학습 이어하기 버튼 클릭시 서버에서 받아오는 시그널
        self.last_learning_btn.clicked.connect(self.lastlearning)
        # # 여기는 받는 부분 그런데 항상 받아야 하므로 쓰레드를 생성한다.
        # self.thread_recv = threading.Thread(target=self.recvMsg, args=())
        # self.thread_recv.start()

        self.connectserver()

    def logout(self):
        reply = QMessageBox.question(self,'메시지','로그아웃 하시겠습니까?')
        if reply == QMessageBox.Yes:
            self.id_label.clear()
            self.name_label.clear()
            self.point_label.clear()
            self.tabWidget.setCurrentIndex(0)
            self.menubar.setVisible(False)
            self.seoul_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.gangwondo_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.chungbuk_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.chungnam_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.gyeongbuk_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.gyeongnam_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.jeonbuk_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.jeonnam_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.jeju_btn.setStyleSheet("background-color: rgb(255, 255, 255)")
            self.seoul_btn.setFont(QFont('Times', 25))
            self.gangwondo_btn.setFont(QFont('Times', 25))
            self.chungbuk_btn.setFont(QFont('Times', 25))
            self.chungnam_btn.setFont(QFont('Times', 25))
            self.gyeongbuk_btn.setFont(QFont('Times', 25))
            self.gyeongnam_btn.setFont(QFont('Times', 25))
            self.jeonbuk_btn.setFont(QFont('Times', 25))
            self.jeonnam_btn.setFont(QFont('Times', 25))
            self.jeju_btn.setFont(QFont('Times', 25))
        else:
            pass

    def main_go(self):
        self.tabWidget.setCurrentIndex(2)

    def ask_board(self):
        self.tabWidget.setCurrentIndex(4)

    def ask_page(self):
        self.tabWidget.setCurrentIndex(5)
    
    def consulting_page(self):
        self.tabWidget.setCurrentIndex(6)

    def lastlearning(self):
        btn = self.sender()
        learningcheck = btn.text()
        self.send_command('/load_learning_user', learningcheck)

    def laststep(self):
        reply = QMessageBox.question(self,'메시지','학습완료를 제출하시겠습니까?')
        if reply == QMessageBox.Yes:
                self.send_command('/save_learning_user', self.informationToServer)
        else:           
            QMessageBox.information(self,'알림', '학습완료를 제출해야 점수와 포인트가 인정이 됩니다.')

    def nextstep(self):
        print(self.nextquiztotal)
        if len(self.nextquiztotal) != 0:
            # a = random.choice(self.nextquiztotal)
            self.quiz_label.setText(self.nextquiztotal[0])
            self.nextquiztotal.pop(0)
        elif len(self.nextquiztotal) == 0:
            QMessageBox.information(self,'알림', f'{self.quiz_area_name_label.text()}지역 문제를 모두 풀었습니다.')
            QMessageBox.information(self,'알림', '학습완료버튼을 클릭하여 지역의 명산왕임을 증명하세요.')


    def learning_submit(self):
        reply = QMessageBox.question(self,'메시지','학습단계를 제출하시겠습니까?')
        if reply == QMessageBox.Yes:
                self.send_command('/save_learning_user', self.informationToServer)
        else:           
            QMessageBox.information(self,'알림', '학습단계를 제출해야 점수와 포인트가 인정이 됩니다.')

    def quiz_last_check(self, quizindex, answer):
        count = 0
        for i in range(1, len(self.informationToServer)):
            for j in range(0, 4):
                if self.informationToServer[i][j] == quizindex:
                    count += 1
        if count == 1:
            if answer == 'O':
                QMessageBox.information(self,'알림', '정답입니다! 축하합니다.')
            else:
                QMessageBox.information(self,'알림', '오답입니다...건투를 빕니다.')

        else:
            QMessageBox.information(self,'알림', '이미 풀었던 문제입니다.')
            print("중복되었습니다.")
            self.informationToServer.pop()
            print(self.informationToServer)

        # for index, value in enumerate(self.informationToServer):
        #     if index>0:
        #         print(index,value[0])
        #         if value[0] == value[0]:
        #             print("중복되었습니다.")

                # if index
                #     print('hi')

                # if value[0] != value[0]:
                #     print("중복되었습니다.")
                # self.quiz_check_user.append(value[0])
                # if len(value[0]) >=2:
                #     print('중복중복')

                # if len(self.quiz_check_user) == len(set(self.quiz_check_user)):
                #     print('hi')
                # else:
                #     self.quiz_check_user.pop()
                #     print(self.quiz_check_user)
        # print(set(self.quiz_check_user))
        # print(self.quiz_check_user)
        # if len(self.quiz_check_user) == len(set(self.quiz_check_user)):
            
        # else:
        #     self.informationToServer.pop()
        #     print(self.informationToServer)

    def quiz_to_server(self, useranswer=str):

        for i in range(len(self.quiz_data)):
            if self.quiz_data[i] == self.quiz_label.text():
                if useranswer == self.quiz_data[i+1]:
                    self.quiztoServer.append(self.quiz_data[i-1][2:]) # 문제인덱스
                    self.quiztoServer.append('O') # 정답유무
                    self.quiztoServer.append(self.quiz_data[i+3][1:-1]) # 문제 점수(포인트)
                    self.endTime = time.time()
                    self.solvingTime = self.endTime - self.startTime
                    self.quiztoServer.append(self.solvingTime)
                    self.startTime = time.time()
                    self.informationToServer.append(self.quiztoServer)
                    self.quiztoServer = []
                    print(self.informationToServer)
                    self.quiz_last_check(self.quiz_data[i-1][2:], 'O')


                    #     print(self.informationToServer)
                    # else:
                    #     QMessageBox.information(self,'알림', '이미 풀었던 문제입니다.')
                    #     self.informationToServer.pop()
                    #     print(self.informationToServer)
        
                else:
                    self.quiztoServer.append(self.quiz_data[i-1][2:]) # 문제인덱스
                    self.quiztoServer.append('X') # 정답유무
                    self.quiztoServer.append(0) # 문제 점수(포인트)
                    self.endTime = time.time()
                    self.solvingTime = self.endTime - self.startTime
                    self.quiztoServer.append(self.solvingTime)
                    self.startTime = time.time()
                    self.informationToServer.append(self.quiztoServer)
                    self.quiztoServer = []
                    print(self.informationToServer)
                    self.quiz_last_check(self.quiz_data[i-1][2:], 'X')



    def quiz_submit(self):
        if self.radioButton_O.isChecked():
            reply = QMessageBox.question(self,'메시지','O로 정답을 제출하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_to_server(self.userAnswer)
            else:           
                pass
        else:
            reply = QMessageBox.question(self,'메시지','X로 정답을 제출하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_to_server(self.userAnswer)
            else:           
                pass

    def quiz_solving(self, rbutton):
        self.userAnswer = rbutton.text()
        print(self.userAnswer)
        # if rbutton is self.radioButton_O:
        #     # print(rbutton.text())
    
        #     return self.radioButton_O
        # else:
        #     print(rbutton.text())
        #     return self.radioButton_X

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
                            try:
                                time.sleep(0.1)
                                total_message = []
                                message = self.sock.recv(self.BUFFER).decode('unicode_escape', 'ignore')
                                if message:
                                    time.sleep(0.1)
                                    total_message.append(message)
                                    time.sleep(0.1)
                                # print(type(message))
                                # print(message)
                                print(total_message)
                                time.sleep(0.1)


                            except:
                                pass

                            # message = json.loads(message)
                            # print(type(message))
                            # print(message)
                            # message.encode('utf-8').decode()
                            # print(message)
                            a = message.split(',')
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
        
        elif command == '/learning_progress':
            print("지난 학습 불러오기에 성공하였습니다.")
            self.load_learning_success(content)
        else:
            pass

    # def ask_success(self, content):
    #     win32api.MessageBox(0,'질문 조회가 완료되었습니다.', '질문조회', 0)
    #     self.askcheck = content
    #     print(self.askcheck)
    def load_learning_success(self, content):
        self.load_learn = content
        win32api.MessageBox(0, '지난 학습 불러오기가 완료되었습니다.', '지난학습', 0)
        for i in range(1, len(self.load_learn)):
            print(self.load_learn[i][2:7])
            if self.load_learn[i][2:7] == self.seoul_btn.text(): # 학습 안한 버튼 
                self.seoul_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.seoul_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.gangwondo_btn.text():
                self.gangwondo_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.gangwondo_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.chungbuk_btn.text():
                self.chungbuk_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.chungbuk_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.chungnam_btn.text():
                self.chungnam_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.chungnam_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.gyeongbuk_btn.text():
                self.gyeongbuk_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.gyeongbuk_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.gyeongnam_btn.text():
                self.gyeongnam_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.gyeongnam_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.jeonbuk_btn.text():
                self.jeonbuk_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.jeonbuk_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.jeonnam_btn.text():
                self.jeonnam_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.jeonnam_btn.setFont(QFont('Times', 25))
            if self.load_learn[i][2:7] == self.jeju_btn.text():
                self.jeju_btn.setStyleSheet("background-color: rgb(0, 170, 255)")
                self.jeju_btn.setFont(QFont('Times', 25))
    
        # print(self.seoul_btn.text())
        # print(self.gangwondo_btn.text())
        # print(self.chungbuk_btn.text())
        # print(self.chungnam_btn.text())
        # print(self.gyeongbuk_btn.text())
        # print(self.gyeongnam_btn.text())
        # print(self.jeonbuk_btn.text())
        # print(self.jeonnam_btn.text())
        # print(self.jeju_btn.text())
    def post_success(self):
        win32api.MessageBox(0, '질문 등록이 완료되었습니다.', '질문등록', 0)
        self.ask_textEdit.clear()

    def login_id_fail(self):
        win32api.MessageBox(0, '로그인에 실패했습니다. ID를 확인 해 주세요.', '로그인실패', 16)

    def login_password_fail(self):
        win32api.MessageBox(0, '로그인에 실패했습니다. 비밀번호를 확인 해 주세요.', '로그인실패', 16)

    def login_success(self, content):
        win32api.MessageBox(0, '로그인에 성공하였습니다. 환영합니다.', '로그인완료', 0)
        self.menubar.setVisible(True)
        self.quiz_data = content

        self.informationToServer = [self.quiz_data[1][4:]] # 유저 인덱스

        self.inforamtion = [self.quiz_data[3], self.quiz_data[4], self.quiz_data[6][:-2]] # 이름, 아이디, 포인트


        self.Namelogin = self.inforamtion[0]
        self.Idlogin = self.inforamtion[1]
        self.Pointlogin = self.inforamtion[2]
        self.id_label.setText(self.Idlogin)
        self.name_label.setText(self.Namelogin)

        self.tabWidget.setCurrentIndex(2)

    def register_success(self):
        win32api.MessageBox(0, '회원가입이 완료되었습니다. 환영합니다.', '등록완료', 0)
        self.register_name.clear()
        self.register_id.clear()
        self.register_password.clear()

    def register_fail(self):
        win32api.MessageBox(0, 'ID가 중복되었습니다. 다른 아이디를 입력 해 주세요.', '중복알림', 48)


    def quiz_receive(self, quiz=list, quiz_total=list, area_name=str):
        
        self.nextquiz = quiz
        self.nextquiztotal = quiz_total
        for i in range(len(self.quiz_data)):
            if self.quiz_data[i] == area_name:
                for j in range(-1, 4):
                    self.nextquiz.append(self.quiz_data[i-j])
        print(self.nextquiz)
        for index, value in enumerate(quiz, start=1):
            if index %5 == 4:
                self.nextquiztotal.append(value)
        print(self.nextquiztotal)
        # a = random.choice(self.nextquiztotal)
        self.quiz_label.setText(self.nextquiztotal[0])
        # for i in range(len(self.nextquiztotal)):
        #     if self.nextquiztotal[i] == self.quiz_label.text():
        self.nextquiztotal.pop(0)
        # self.nextquiztotal.pop(a)
        print(self.nextquiztotal)
        # quiz_total.remove(a)
        
        self.tabWidget.setCurrentIndex(3)
        self.startTime = time.time()
        self.quiztoServer = []
        # self.check_quiz = quiz
        # self.check_quiztotal = quiz_total
        return self.nextquiztotal, self.nextquiz

    def quiz_request(self):
        # 버튼 객체 얻기
        btn = self.sender()
        self.quize_name = btn.text()

        if self.quize_name == '서울/경기':
            reply = QMessageBox.question(self, '메시지', '서울/경기 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:

                self.quiz_area_name_label.setText(self.quize_name)
                self.Seoul_quiz = []
                self.Seoul_quiz_total = []
                self.quiz_receive(self.Seoul_quiz, self.Seoul_quiz_total, ' "서울/경기"')

                
            else:
                pass

        elif self.quize_name == '강원도"]':
            reply = QMessageBox.question(self, '메시지', '강원 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_area_name_label.setText(self.quize_name)
                self.Gangwon_quiz = []
                self.Gangwon_quiz_total = []
                self.quiz_receive(self.Gangwon_quiz, self.Gangwon_quiz_total, ' "강원도"')
            else:
                pass


        elif self.quize_name== '충청북도"':
            reply = QMessageBox.question(self,'메시지','충청북도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_area_name_label.setText(self.quize_name)
                self.Chungbuk_quiz = [] 
                self.Chungbuk_quiz_total = []
                self.quiz_receive(self.Chungbuk_quiz, self.Chungbuk_quiz_total, ' "충청북도"')

            else:
                pass

        elif self.quize_name== '충청남도"':
            reply = QMessageBox.question(self,'메시지','충청남도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_area_name_label.setText(self.quize_name)
                self.Chungnam_quiz = []
                self.Chungnam_quiz_total = [] 
                self.quiz_receive(self.Chungnam_quiz, self.Chungnam_quiz_total, ' "충청남도"')
            else:
                pass


        elif self.quize_name == '경상북도"':
            reply = QMessageBox.question(self, '메시지', '경상북도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:

                self.quiz_area_name_label.setText(self.quize_name)
                self.Gyeongbuk_quiz = []
                self.Gyeongbuk_quiz_total = []
                self.quiz_receive(self.Gyeongbuk_quiz, self.Gyeongbuk_quiz_total, ' "경상북도"')

            else:
                pass

        elif self.quize_name == '경상남도"':
            reply = QMessageBox.question(self, '메시지', '경상남도 지역 명산에 도전하시겠습니까?')

            if reply == QMessageBox.Yes:
                self.quiz_area_name_label.setText(self.quize_name)
                self.Gyeongnam_quiz = []
                self.Gyeongnam_quiz_total = []
                self.quiz_receive(self.Gyeongnam_quiz, self.Gyeongnam_quiz_total, ' "경상남도"')

            else:
                pass
        elif self.quize_name == '전라북도"':
            reply = QMessageBox.question(self, '메시지', '전라북도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_area_name_label.setText(self.quize_name)
                self.Jeonbuk_quiz = []
                self.Jeonbuk_quiz_total = []
                self.quiz_receive(self.Jeonbuk_quiz, self.Jeonbuk_quiz_total, ' "전라북도"')

            else:
                pass
        elif self.quize_name == '전라남도"':
            reply = QMessageBox.question(self, '메시지', '전라남도 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_area_name_label.setText(self.quize_name)
                self.Jeonnam_quiz = []
                self.Jeonnam_quiz_total = []
                self.quiz_receive(self.Jeonnam_quiz, self.Jeonnam_quiz_total, ' "전라남도"')

            else:
                pass
        else:
            reply = QMessageBox.question(self, '메시지', '제주 지역 명산에 도전하시겠습니까?')
            if reply == QMessageBox.Yes:
                self.quiz_area_name_label.setText(self.quize_name)
                self.Jeju_quiz = []
                self.Jeju_quiz_total = []
                self.quiz_receive(self.Jeju_quiz, self.Jeju_quiz_total, ' "제주도"')

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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StudentWindow()
    win.show()
    app.exec_()
