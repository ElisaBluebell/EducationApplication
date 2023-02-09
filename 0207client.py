import json
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
# import jason
import datetime
from socket import *
import threading



# ui파일 연결
form_class = uic.loadUiType("tracking.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        pixmap = QPixmap("C:/Users/sw/PycharmProjects/EducationApplication/등산.png")  # 코드 3줄 ui에 이미지를 넣을 수 있음
        pixmap = pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation) # 코드 3줄 ui에 이미지를 넣을 수 있음
        self.login_label.setPixmap(pixmap)                                            # 코드 3줄 ui에 이미지를 넣을 수 있음

        self.initialize_socket()
        self.Map_label.setPixmap(QPixmap('100대명산지도.png'))  # ui에 이미지를 넣을 수 있음
        self.background_label.setPixmap(QPixmap('Background.png')) # ui에 이미지를 넣을 수 있음
        # self.login_btn.clicked.connect(self.login) # 로그인 버튼을 누르면
        # self.sign_up.clicked.connect(self.join_us) # 회원가입(1tab) 버튼을 누르면
        # self.quiz_tableWidget
        self.register_signup_btn.clicked.connect(self.sign)  # 회원가입(2tab) 버튼을 누르면
        # self.check_ID_btn.clicked.connect(self.check_ID)  # 아이디 중복확인을 누르면
        # self.id_lineedit.SetText(self.id_lineedit)

        #### 문제풀이에 관한 데이터 요청 버튼 <도별> ####
        # self.seoul_btn.clicked.connect(self.quiz_request)
        # self.gangwondo_btn.clicked.connect(self.quiz_request)
        # self.chungbuk_btn.clicked.connect(self.quiz_request)
        # self.chungnam_btn.clicked.connect(self.quiz_request)
        # self.gyeongbuk_btn.clicked.connect(self.quiz_request)
        # self.gyeongnam_btn.clicked.connect(self.quiz_request)
        # self.jeonbuk_btn.clicked.connect(self.quiz_request)
        # self.jeonnam_btn.clicked.connect(self.quiz_request)
        # self.jeju_btn.clicked.connect(self.quiz_request)

        # self.connectserver()
        self.show()



    def initialize_socket(self):
        # ip = '127.0.0.1'
        ip = '10.10.21.121'  # 컴퓨터 ip
        port = 9000
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def quiz_request(self):
        # 버튼 객체 얻기
        btn = self.sender() ###?

        self.quiz_name = btn.text()
        if self.quize_name == '서울/경기':
            self.send_commang('/quize_seoul', self.quize_name)
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



    def sign(self):
        list = ['/register_user', [self.combo_2.currentText(), self.name.text(), self.ID.text(), self.ps_3.text()]]
        self.client_socket.send(json.dumps(list).encode())
        incoming_message = self.client_socket.recv(1024)
        a = json.loads(incoming_message).decode()
        print(a)
        # con = pymysql.connect(host='localhost', user='ElisaBluebell', password='1234',
        #                       db='aducationapplication', charset='utf8')  # 한글처리 (charset = 'utf8')
        #
        # # STEP 3: Connection 으로부터 Cursor 생성
        # cur = con.cursor()
        #
        # # STEP 4: SQL문 실행 및 Fetch
        # sql = f"insert into account(class, user_name, user_id, user_password) values('', '', '{self.id_3.text()}', '{self.ps_3.text()}')"
        # cur.execute(sql)
        # con.commit()
        # self.QnA_tabWidget.setCurrentIndex(0)
    #
    #
    # def check_ID(self):
    #     self.id_check = False
    #     self.check_label.setText('중복 확인을 눌러주세요.')
    #
    # def join_us(self):
    #     self.QnA_tabWidget.setCurrentIndex(1)
    #
    # def login(self): # 로그인 정보 전달
    #     self.id = self.id_lineedit.text()
    #     self.pw = self.pw_lineedit.text()
    #     self.loginlist = [self.id, self.pw]
    #
    #     print(self.id)
    #     print(self.pw)
    #
    #     if '' not in self.loninlist:
    #         self.send_command('/login_teacher', self.loginlist)
    #
    #     if self.id == '' or self.pw == '':
    #         self.login_label_4.setText('아이디와 비밀번호를 입력해주세요.')
    #         return

        # 서버에 전달하기위한 딕셔너리 생성
        # login = {'id' : id, 'pw' : pw}
        # 서버에 데이터를 전송하기 위한 send_data 함수 호출(딕셔너리 생성자)
        # self.send_data(login, 'log')

    # def join(self):  # 회원가입
    #     print('회원가입')
    #     if self.id_check == True:
    #         new_user = (self.ID.text(), self.ps_3.text())
    #         msg = f"ID: {new_user[0]}\nPW: {new_user[1]}가입하시겠습니까?"
    #
    #         # 가입 의사 확인 메시지박스
    #         reply = QMessageBox.question(self, '회원가입', msg,
    #                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #         if reply == QMessageBox.Yes:
    #             # 서버에 회원가입을 위한 데이터를 전달
    #             self.send_data(new_user, 'new')  # 튜플 new_user, 식별자 'new'
    #             QMessageBox.information(self, '완료', '가입이 완료되었습니다.')
    #             print('가입 완료')
    #
    #             # 회원가입 입력칸 초기화
    #             self.ID.setText('')
    #             self.ps_3.setText('')
    #             # self.acount_tabWidget.setCurrentIndex(0)
    #             self.id_check = False

    # def send_data(self, data, idf:str): # 데이터를 전송하는 함수
    #     # DB에 넘겨줄 데이터를 포함하는 딕셔너리 data와 식별자 idf인자로 받음
    #     '''
    #     log : 로그인
    #     acc : 회원가입
    #
    #     '''
    #
    #     print('send_data -- ', end = '')
    #     data = json.dumps(data) # 딕셔너리를 바이너리화 하는 json.dumps 메서드
    #     print('1', end='-')
    #     msg = idf + data # 식별자{딕셔너리 내용}
    #     print('2', end='-')
    #     self.client_socket.send(msg.encode()) # 바이너리를 바이트로 바꿔서 전송
    #     print(f'{msg}전송')


    # def send_chat(self):
    #     # senders_name = self.user_name_line_edit_1p.text() #ui사용자이름
    #     senders_name = self.user[0] # 윗줄의 코드를 수정
    #     print(1)
    #     data = self.signal_textEdit.toPlainText() #
    #     print(2)
    #     self.receive_listWidget.addItem(f'{senders_name} : {data}') #ui
    #     print(3)
    #     message = (f'{senders_name} : {data}').encode('utf-8')
    #     print(4)
    #     self.client_socket.send(message)
    #     print(5)
    #     self.signal_textEdit.clear()
    #     print(6)
        # 서버의 응답을 받는 코드

    def receive_message(self, so):
        while True:
            buf = so.recv(9000)
            if not buf:  # 연결종료
                break

            # recv_data = buf.decode()  # 서버에서 응답한 데이터를 decode
            # print(recv_data)
            # request = recv_data[0:3]  # 서버의 응답에서 식별자 구분
            #
            # if len(recv_data) > 3:  # 식별자 이외의 데이터가 존재한다면 데이터 할당
            #     self.last_request = recv_data[3:]
            #
            # else:  # 없다면 None (서버에서의 DB 조회 결과가 None 인 경우)
            #     self.last_request = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    # cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    # cThread.start()
    app.exec_()
