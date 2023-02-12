import json
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
import datetime
from socket import *
import threading
import time
# ui파일 연결
form_class = uic.loadUiType("tracking.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        pixmap = QPixmap("C:/Users/sw/PycharmProjects/EducationApplication/등산.png")  # 코드 3줄 ui에 이미지를 넣을 수 있음
        pixmap = pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 코드 3줄 ui에 이미지를 넣을 수 있음
        self.login_label.setPixmap(pixmap)  # 코드 3줄 ui에 이미지를 넣을 수 있음

        self.initialize_socket()

        cThread = threading.Thread(target=self.receive_message, args=(self.client_socket,))
        cThread.start()
        self.chat_able = 0
        self.gangwon_btn.setStyleSheet('강원도.png')
        self.Map_label.setPixmap(QPixmap('100대명산지도.png'))  # ui에 이미지를 넣을 수 있음
        self.background_label.setPixmap(QPixmap('Background.png'))  # ui에 이미지를 넣을 수 있음
        self.login_btn.clicked.connect(self.login)  # 로그인 버튼을 누르면
        self.sign_up.clicked.connect(self.join_us)  # 회원가입(1tab) 버튼을 누르면
        self.register_signup_btn.clicked.connect(self.sign)  # 회원가입(2tab) 버튼을 누르면
        self.sign_up.clicked.connect(self.sign_)  # 1p의 회원가입을 누르면
        # self.check_ID_btn.clicked.connect(self.check_ID)  # 아이디 중복확인을 누르면
        self.qna_tableWidget.cellDoubleClicked.connect(self.qna)
        self.answer_lineedit.returnPressed.connect(self.send_)
        self.quizadd_lineedit.returnPressed.connect(self.update)
        self.o_btn.clicked.connect(self.change_o)
        self.x_btn.clicked.connect(self.change_x)
        self.a = ''
        self.send_btn.clicked.connect(self.send_)
        self.score_btn.clicked.connect(self.student_score)
        self.input_chat.returnPressed.connect(self.send_chat) ###############################
        self.user_select.currentTextChanged.connect(self.request_past_chat_data)


        #### 문제풀이에 관한 추가 데이터 요청 버튼 <도별> ####
        self.gangwon_addbtn.clicked.connect(self.gangwon_add)
        self.gyeonggi_addbtn.clicked.connect(self.gyeonggi_add)
        self.chungbuk_addbtn.clicked.connect(self.chungbuk_add)
        self.chungnam_addbtn.clicked.connect(self.chungnam_add)
        self.gyeongbuk_addbtn.clicked.connect(self.gyeongbuk_add)
        self.gyeongnam_addbtn.clicked.connect(self.gyeongnam_add)
        self.jeonbuk_addbtn.clicked.connect(self.jeonbuk_add)
        self.jeonnam_addbtn.clicked.connect(self.jeonnam_add)
        self.jeju_addbtn.clicked.connect(self.jeju_add)
        self.b = ''
        # self.show()

        #### 문제풀이에 관한 데이터 요청 버튼 <도별> ####
        self.gangwon_btn.clicked.connect(self.gangwon)
        self.gyeonggi_btn.clicked.connect(self.gyeonggi)
        self.chungbuk_btn.clicked.connect(self.chungbuk)
        self.chungnam_btn.clicked.connect(self.chungnam)
        self.gyeongbuk_btn.clicked.connect(self.gyeongbuk)
        self.gyeongnam_btn.clicked.connect(self.gyeongnam)
        self.jeonbuk_btn.clicked.connect(self.jeonbuk)
        self.jeonnam_btn.clicked.connect(self.jeonnam)
        self.jeju_btn.clicked.connect(self.jeju)
        self.chat_client()
        # self.connectserver()
        self.show()

    def initialize_socket(self):
        # ip = '127.0.0.1'
        ip = '10.10.21.121'  # 컴퓨터 ip
        port = 9000
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def gangwon_add(self):
        self.b = '/gangwon_add'
    def gyeonggi_add(self):
        self.b = '/seoul_add'
    def chungbuk_add(self):
        self.b ='/chungbuk_add'
    def chungnam_add(self):
        self.b = '/chungnam_add'
    def gyeongbuk_add(self):
        self.b = '/gyeongbuk_add'
    def gyeongnam_add(self):
        self.b = '/gyeongnam_add'
    def jeonbuk_add(self):
        self.b = '/jeonbuk_add'
    def jeonnam_add(self):
        self.b = '/jeonnam_add'
    def jeju_add(self):
        self.b = '/jeju_add'
    def gangwon(self):
        self.send_command('/quize_gangwon', '')

    def gyeonggi(self):
        self.send_command('/quize_seoul', '')

    def chungbuk(self):
        self.send_command('/quize_chungbuk', '')

    def chungnam(self):
        self.send_command('/quize_chungnam', '')

    def gyeongbuk(self):
        self.send_command('/quize_gyeongbuk', '')

    def gyeongnam(self):
        self.send_command('/quize_gyeongnam', '')

    def jeonbuk(self):
        self.send_command('/quize_jeonbuk', '')

    def jeonnam(self):
        self.send_command('/quize_jeonnam', '')

    def jeju(self):
        self.send_command('/quize_jeju', '')

    def qna(self):
        self.send_command('/qna', '')

    def student_score(self):
        self.send_command('/student_score', '')
        print('학생들 점수 보내주세요.')

    def sign_(self):
        self.tabWidget.setCurrentIndex(1)

    def login(self):
        self.id = self.teacher_id.text()
        self.password = self.teacher_pw.text()
        self.loginlist = [self.id, self.password]
        if '' not in self.loginlist:
            self.send_command('/login_teacher', self.loginlist)

    def login_success(self, content):
        self.tabWidget.setCurrentIndex(2)
        self.user_name = content
        self.send_command('/request_login_member_list', '')


    def login_id_fail(self):
        print("로그인에 실패했습니다.")
        self.login_label_4.text('로그인에 실패했습니다. 아이디와 비밀번호를 확인 해 주세요')

    def send_command(self, command, content):
        msg = [command, content]
        data = json.dumps(msg)
        print(f'보낸 메시지: {data} [{datetime.datetime.now()}]')
        self.client_socket.send(data.encode())

    def sign(self):
        list = ['/register_user', [self.combo_2.currentText(), self.name.text(), self.ID.text(), self.ps_3.text()]]
        self.join_label.setText("회원가입이 완료되었습니다.")
        self.client_socket.send(json.dumps(list).encode())

    def check_ID(self):
        self.id_check = False
        self.check_label.setText('중복 확인을 눌러주세요.')

    def join_us(self):
        self.tabWidget.setCurrentIndex(1)

    def send_(self):
        self.answer = self.answer_lineedit.text()  # 라인에딧안에 글자를 적으면
        pyo = self.qna_tableWidget.currentColumn()
        rows = self.qna_tableWidget.currentRow()
        # if self.qna_tableWidget.currentColumn() != 4:
        if self.qna_tableWidget.currentColumn() != 4:  # 4번째 열이 아닐경우에는
            pass  # 패스
        else:
            self.qna_tableWidget.setItem(rows, 4, QTableWidgetItem(self.answer))
            send = '/answer_send', [self.answer, rows+1]
            self.client_socket.send(json.dumps(send).encode())

    # def score_label(self):
    #     self.score_label.setText(self.gyu)
    def change_o(self):
        self.a = 'O'
        print('self.a: ', self.a)
    def change_x(self):
        self.a = 'X'
        print('self.a: ', self.a)
    def update(self):
        quiz_up = self.quizadd_lineedit.text()  # 라인에딧안에 글자를 적으면
        send = '/update_send', [quiz_up, self.a, self.b]
        self.client_socket.send(json.dumps(send).encode())
        print('성공')

    def receive_message(self, so):  # 서버에서 메시지를(?) 받는함수
        while True:
            buf = so.recv(8192)
            if not buf:  # 연결종료
                break

            # recv_data = buf.decode()  # 서버에서 응답한 데이터를 decode
            recv_data = buf.decode()
            request = eval(recv_data)  # 서버의 응답에서 식별자 구분
            command = request[0]
            content = request[1]
            print(f'command: {command}')
            print(f'content: {content}')
            if command == '/login_success':
                self.login_success(content)
            elif command == '/login_id_fail':
                self.login_label_4.setText('아이디와 비밀번호를 확인 해 주세요.')
            elif command == '/login_password_fail':
                self.login_label_4.setText('아이디와 비밀번호를 확인 해 주세요.')
            elif command == '/location_quiz':
                print(content[0][1])
                # self.qt_textEdit.setPlainText("content[0][1]") ###
                # self.quiz_textBrowser
                # self.quiz_tableWidget.setItem(0, 0, QTableWidgetItem(content[0][1])) # 오류는 안나는데 테이블위젯에 안나타남
                self.quiz_label.setText(content[0][1])
                self.quiz_label.setWordWrap(True)  # 자동 줄바꿈
                print(12123123)
                # print(self.quiz_textBrowser)
            elif command == '/whole_qna_data':
                for i in range(len(content)):
                    for j in range(len(content[i])):
                        content[i][j] = str(content[i][j])
                        content[i][j] = content[i][j].replace('\n', ' ')
                        self.qna_tableWidget.setItem(i, j, QTableWidgetItem(content[i][j]))
                        # self.qna_tableWidget.setFixedSize(1000, 2000) # 테이블 위젯 사이즈
                        self.qna_tableWidget.horizontalHeader().setVisible(True)  # 칼럼헤더 보이기
                        table = self.qna_tableWidget  # 내용에 따라 열너비 자동조정
                        header = table.horizontalHeader()  # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 내용에 따라 열너비 자동조정
            elif command == '/register_fail':
                self.join_label.setText("이미 등록되어 있는 회원입니다.")
            elif command == '/quiz_inserted':
                self.update_label.setText("문제 업데이트 완료")
            elif command == '/student_score':
                col = 0
                self.score_tableWidget.setRowCount(len(content))
                # self.score_tableWidget.setcolumnCount(len(content))
                # for s in range(len(content[0])):  # 점수:
                for s in range(len(content[0])):
                    self.score_tableWidget.setItem(0, 0, QTableWidgetItem(str(content[2][0]))) # 이름은 0번째
                    self.score_tableWidget.setItem(0, 1, QTableWidgetItem(str(content[2][1][0][0])))
                    self.score_tableWidget.setItem(0, 2, QTableWidgetItem(str(content[2][1][1][0])))
                    self.score_tableWidget.setItem(0, 3, QTableWidgetItem(str(content[2][1][2][0])))
                    self.score_tableWidget.setItem(0, 4, QTableWidgetItem(str(content[2][1][3][0])))
                    self.score_tableWidget.setItem(0, 5, QTableWidgetItem(str(content[2][1][4][0])))
                    self.score_tableWidget.setItem(0, 6, QTableWidgetItem(str(content[2][1][5][0])))
                    self.score_tableWidget.setItem(0, 7, QTableWidgetItem(str(content[2][1][6][0])))
                    self.score_tableWidget.setItem(0, 8, QTableWidgetItem(str(content[2][1][7][0])))
                    self.score_tableWidget.setItem(0, 9, QTableWidgetItem(str(content[2][1][8][0])))

                for i in range(len(content[0])):  # 점수:
                    self.score_tableWidget.setItem(1, 0, QTableWidgetItem(str(content[11][0]))) # 이름은 0번째
                    self.score_tableWidget.setItem(1, 1, QTableWidgetItem(str(content[11][1][0][0])))
                    self.score_tableWidget.setItem(1, 2, QTableWidgetItem(str(content[11][1][1][0])))
                    self.score_tableWidget.setItem(1, 3, QTableWidgetItem(str(content[11][1][2][0])))
                    self.score_tableWidget.setItem(1, 4, QTableWidgetItem(str(content[11][1][3][0])))
                    self.score_tableWidget.setItem(1, 5, QTableWidgetItem(str(content[11][1][4][0])))
                    self.score_tableWidget.setItem(1, 6, QTableWidgetItem(str(content[11][1][5][0])))
                    self.score_tableWidget.setItem(1, 7, QTableWidgetItem(str(content[11][1][6][0])))
                    self.score_tableWidget.setItem(1, 8, QTableWidgetItem(str(content[11][1][7][0])))
                    self.score_tableWidget.setItem(1, 9, QTableWidgetItem(str(content[11][1][8][0])))
                gyu = content[2][1][0][0]
                self.score_label.setText(str(gyu))
                ui = int(content[11][1][2][0]) + int(content[11][1][8][0])
                self.score_label_1.setText(str(ui))
                # print(content[2][1][0][0])
                # print(content[2][1][1][0])

            elif content == '':
                pass

            elif command == '/login_user_list':
                self.renew_user_list(content)

            # 현재 접속중인 유저명 저장, 학생 로그인의 경우 user_name 재설정 필요
            elif command == '/login_success':
                self.user_name = content

            elif command == '/get_user_name':
                self.renew_user_list(content)

            elif command == '/get_past_chat':
                self.print_past_chat(content)

            elif command == '/new_chat':
                self.receive_chat(content)

            else:
                pass
    def chat_client(self):
        self.send.setText('전송')
        self.send.clicked.connect(self.send_chat)

    # 콤보박스 유저 목록 최신화
    def renew_user_list(self, content):
        # 유저 목록 초기화
        self.user_select.clear()
        connectable_user_list = content

        # 채팅 가능 유저가 있을 경우
        if connectable_user_list:
            # 채팅 가능 상태로 돌림
            self.chat_able = 1
            # 유저명을 콤보박스에 삽입
            for connectable_user in connectable_user_list:
                self.user_select.addItem(connectable_user)

        else:
            # 콤보박스에 상담 불가능을 표시하는 아이템 추가
            self.user_select.addItem('지금은 상담이 불가능합니다.')
            # 상담 불가 상태로 돌림
            self.chat_able = 0

    # 상담 가능 상태일 시 채팅 윈도우를 초기화하고 지난 채팅 불러오기
    def request_past_chat_data(self):
        self.chat_window.clear()
        # if self.chat_able == 1:
        # content = [현재 접속중인 유저명, 콤보박스에서 선택한 유저명]
        self.send_command('/request_past_chat_data', [self.user_name, self.user_select.currentText()])
        # print('유저명: ', self.user_select.currentText())

    # 지난 채팅 출력 기능
    def print_past_chat(self, past_chat):
        # 서버로부터 받아온 지난 채팅 리스트의 길이만큼 반복해서 출력
        if past_chat:
            for i in range(len(past_chat)):
                self.chat_window.addItem(past_chat[i][0])

        # 이후 스크롤 바닥으로
        time.sleep(0.01)
        self.chat_window.scrollToBottom()

    # 채팅 전송 기능
    def send_chat(self):
        # if self.chat_able == 1:
        chat_to_send = self.input_chat.text()
        # 채팅창 초기화
        self.input_chat.clear()

        chat_data = [self.user_name, self.user_select.currentText(), chat_to_send]
        self.send_command('/new_chat', chat_data)

    def receive_chat(self, content):
        self.chat_window.addItem(content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    # cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    # cThread.start()
    app.exec_()
