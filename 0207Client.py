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



# ui파일 연결
form_class = uic.loadUiType("tracking.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        pixmap = QPixmap("C:/Users/sw/PycharmProjects/EducationApplication/등산.png")  # 코드 3줄 ui에 이미지를 넣을 수 있음
        pixmap = pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation) # 코드 3줄 ui에 이미지를 넣을 수 있음
        self.login_label.setPixmap(pixmap)                                            # 코드 3줄 ui에 이미지를 넣을 수 있음

        self.initialize_socket()

        cThread = threading.Thread(target=self.receive_message, args=(self.client_socket,))
        cThread.start()

        self.Map_label.setPixmap(QPixmap('100대명산지도.png'))  # ui에 이미지를 넣을 수 있음
        self.background_label.setPixmap(QPixmap('Background.png')) # ui에 이미지를 넣을 수 있음
        self.login_btn.clicked.connect(self.login) # 로그인 버튼을 누르면
        self.sign_up.clicked.connect(self.join_us) # 회원가입(1tab) 버튼을 누르면
        self.register_signup_btn.clicked.connect(self.sign)  # 회원가입(2tab) 버튼을 누르면
        self.sign_up.clicked.connect(self.sign_) # 1p의 회원가입을 누르면
        self.check_ID_btn.clicked.connect(self.check_ID)  # 아이디 중복확인을 누르면
        self.qna_tableWidget.cellDoubleClicked.connect(self.qna)
        self.answer_lineedit.returnPressed.connect(self.send)
        self.send_btn.clicked.connect(self.send)
        # self.answer_lineedit.Text(self.send)
        # self.id_lineedit.SetText(self.id_lineedit)

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
        # self.connectserver()
        self.show()

    def initialize_socket(self):
        # ip = '127.0.0.1'
        ip = '10.10.21.121'  # 컴퓨터 ip
        port = 9000
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))

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

    def sign_(self):
        self.tabWidget.setCurrentIndex(1)

    def login(self):
        self.id = self.teacher_id.text()
        self.password = self.teacher_pw.text()
        self.loginlist = [self.id, self.password]
        if '' not in self.loginlist:
            self.send_command('/login_teacher', self.loginlist)

    def login_success(self):
        self.tabWidget.setCurrentIndex(2)

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

    def send(self):
        print(123)
        answer = self.answer_lineedit.text() # 라인에딧안에 글자를 적으면
        pyo = self.qna_tableWidget.currentColumn()
        rows = self.qna_tableWidget.currentRow()
        # if self.qna_tableWidget.currentColumn() != 4:
        if self.qna_tableWidget.currentColumn() != 4: # 4번째 열이 아닐경우에는
            pass                                      # 패스
        else:
            self.qna_tableWidget.setItem(rows, 4, QTableWidgetItem(answer))
            send = '/answer_send', [answer, rows]
            print(111)
            self.client_socket.send(json.dumps(send).encode())
            print('성공')

    def receive_message(self, so): # 서버에서 메시지를(?) 받는함수
        while True:
            buf = so.recv(8192)
            if not buf:  # 연결종료
                break

            recv_data = buf.decode()  # 서버에서 응답한 데이터를 decode

            request = eval(recv_data)  # 서버의 응답에서 식별자 구분
            command = request[0]
            content = request[1]
            print(f'command: {command}')
            print(f'content: {content}')
            if command == '/login_success':
                self.login_success()
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
                self.quiz_label.setWordWrap(True) # 자동 줄바꿈
                print(12123123)
                # print(self.quiz_textBrowser)
            elif command == '/whole_qna_data':
                for i in range(len(content)):
                    for j in range(len(content[i])):
                        content[i][j] = str(content[i][j])
                        content[i][j] = content[i][j].replace('\n', ' ')
                        self.qna_tableWidget.setItem(i, j, QTableWidgetItem(content[i][j]))
                        # self.qna_tableWidget.setFixedSize(1000, 2000) # 테이블 위젯 사이즈
                        self.qna_tableWidget.horizontalHeader().setVisible(True) # 칼럼헤더 보이기
                        table = self.qna_tableWidget # 내용에 따라 열너비 자동조정
                        header = table.horizontalHeader() # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # 내용에 따라 열너비 자동조정
                        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # 내용에 따라 열너비 자동조정


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    # cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    # cThread.start()
    app.exec_()