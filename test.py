from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QWidget, QPushButton, QApplication
import sys
import server_tool as st

# a = QTableWidget()
# a.currentRow()
# a.currentColumn()
# a.setItem(0, 0, QTableWidgetItem('11'))
#
# b = QLabel
#
# b.text

# xml_string = st.get_database_from_url('http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?serviceKey=yn8uwUR3eheqowtPnA9QRTQ9i8mYGhGEetp6HDG1hMhCeH9%2BNJFN6WlIM1AzfgrZB59syoKUT1rAVveE9J6Okg%3D%3D&searchMtNm=&searchArNm=&pageNo=1&numOfRows=100')
# raw_data = st.xml_to_json(xml_string)

# self.mntnm, self.aeatreason, self.overview, self.details = self.get_useful_data(raw_data)
# st.null_to_zero([self.mntnm, self.aeatreason, self.overview, self.details])


# for i in range(len(self.mntnm)):
#     print('length: ', len(self.mntnm))
#     print('i + 1: ', i + 1)
#     print('mntnm: ', self.mntnm[i])
#     print('aeatreason: ', self.aeatreason[i])
#     print('overview: ', self.overview[i])
#     print('details: ', self.details[i])
#     sql = f'''INSERT INTO education_data VALUES({i + 1}, "{self.mntnm[i]}", "{self.aeatreason[i]}", "{self.overview[i]}", "{self.details[i]}")'''
#     st.execute_db(sql)

# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.o_btn = QPushButton(self)
#         self.x_btn = QPushButton(self)
#         self.o_btn.setText('o')
#         self.x_btn.setText('x')
#         self.o_btn.setGeometry(20, 20, 20, 20)
#         self.x_btn.setGeometry(40, 40, 20, 20)
#         self.setGeometry(0, 0, 400, 400)
#         self.o_btn.clicked.connect(self.change_to_o)
#         self.x_btn.clicked.connect(self.change_to_x)
#         self.a = ''
#
#     def change_to_o(self):
#         self.a = 'o'
#         print('self.a: ', self.a)
#
#     def change_to_x(self):
#         self.a = 'x'
#         print('self.a: ', self.a)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     app.exec_()

# print('/gangwon_add'[1:-4])
#
# user_index = []
# user_score_data = []
# sql = 'SELECT user_index FROM user_account WHERE class="학생"'
# user_number = st.execute_db(sql)
# for i in range (len(user_number)):
#     user_index.append(user_number[i][0])
# print(user_index)
# for i in user_index:
#     sql = f'SELECT user_name FROM user_account WHERE user_index={i}'
#     user_name = st.execute_db(sql)[0][0]
#     sql = f'SELECT SUM(a.correct), SUM(a.solve_datetime), b.area_name FROM ss AS a INNER JOIN quiz AS b ON a.quiz_index=b.quiz_index WHERE a.user_index={i} GROUP BY b.area_name;'
#     user_score = st.execute_db(sql)
#     user_data = [user_name, user_score]
#     user_score_data.append(user_data)
#
# print(user_score_data)
#
#
# a = (1, 2, [3, 2])
# b = [1, 2, (3, 2)]
#
# print(a[2][0])
# print(b[2][0])


# ((0.0, 0.0, '전라남도'), (0.0, 0.0, '경상남도'), (0.0, 0.0, '서울/경기'), (0.0, 0.0, '경상북도'), (0.0, 0.0, '충청북도'), (0.0, 0.0, '충청남도'), (0.0, 0.0, '제주도'), (0.0, 0.0, '전라북도'), (0.0, 0.0, '강원도'))
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
        pixmap = pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 코드 3줄 ui에 이미지를 넣을 수 있음
        self.login_label.setPixmap(pixmap)  # 코드 3줄 ui에 이미지를 넣을 수 있음

        self.initialize_socket()

        cThread = threading.Thread(target=self.receive_message, args=(self.client_socket,))
        cThread.start()

        self.Map_label.setPixmap(QPixmap('100대명산지도.png'))  # ui에 이미지를 넣을 수 있음
        self.background_label.setPixmap(QPixmap('Background.png'))  # ui에 이미지를 넣을 수 있음
        self.login_btn.clicked.connect(self.login)  # 로그인 버튼을 누르면
        self.sign_up.clicked.connect(self.join_us)  # 회원가입(1tab) 버튼을 누르면
        self.register_signup_btn.clicked.connect(self.sign)  # 회원가입(2tab) 버튼을 누르면
        self.sign_up.clicked.connect(self.sign_)  # 1p의 회원가입을 누르면
        self.check_ID_btn.clicked.connect(self.check_ID)  # 아이디 중복확인을 누르면
        self.qna_tableWidget.cellDoubleClicked.connect(self.qna)
        self.answer_lineedit.returnPressed.connect(self.send)
        self.quizadd_lineedit.returnPressed.connect(self.update)
        self.o_btn.clicked.connect(self.change_o)
        self.x_btn.clicked.connect(self.change_x)
        self.a = ''
        self.send_btn.clicked.connect(self.send)
        self.score_btn.clicked.connect(self.student_score)


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
                for i in range(len(content)):
                    self.score_tableWidget.setItem(i, 0, QTableWidgetItem(str(content[0][1][0][0]))) # 행열 QTableWidgetItem(str(content[0][1][8][0]
                    # self.score_tableWidget.setItem(i, 0, QTableWidgetItem(str(content[0][2])))

                    # send = '/answer_send', [self.answer, content[0]]


        # self.answer = self.answer_lineedit.text()  # 라인에딧안에 글자를 적으면
        # pyo = self.score_tableWidget.currentColumn()
        # rows = self.score_tableWidget.currentRow()
        # # if self.qna_tableWidget.currentColumn() != 4:
        # if self.qna_tableWidget.currentColumn() != 4:  # 4번째 열이 아닐경우에는
        #     pass  # 패스
        # else:
        #     self.score_tableWidget.setItem(rows, 4, QTableWidgetItem(self.answer))
        #     send = '/answer_send', [self.answer, rows+1]
        #     self.client_socket.send(json.dumps(send).encode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    # cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    # cThread.start()
    app.exec_()