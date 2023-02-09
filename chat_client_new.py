# GUI 채팅 클라이언트
import json
from socket import *
import sys

import pymysql
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import threading

form_class = uic.loadUiType("chat11.ui")[0]
class WindowClass(QMainWindow, form_class):
    user = None # (이름, 번호, 비밀번호) 튜플
    last_request = None

    new_user = None # 가입을 시도하는 계정정보 튜플
    id_check = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(600,100)
        self.initialize_socket()

        self.send_btn.clicked.connect(self.send_chat) #ui메시지전송버튼
        self.stackedWidget.setCurrentIndex(0) #스택위젯 0p 고정
        self.acount_tabWidget.setCurrentIndex(0) # 로그인/가입 탭위젯 0

        self.chat_open_btn.clicked.connect(self.login) # 로그인
        self.check_btn.clicked.connect(self.check_phone) # 번호 중복확인
        self.phone_lineEdit.textChanged.connect(self.check_phone2) # 중복확인2
        self.join_btn.clicked.connect(self.join) # 회원가입

        self.chat_add_btn.clicked.connect(self.new_chatroom) #채팅방 생성 버튼
        self.chat_search_btn.clicked.connect(self.list_up_room) # 채팅방 조회 버튼

        # lineEdit 입력 제한
        phone_re = QtCore.QRegExp("[0-9]{10,11}") # 휴대폰 번호
        self.phone_lineEdit.setValidator(QtGui.QRegExpValidator(phone_re))
        self.user_phone_lineEdit.setValidator(QtGui.QRegExpValidator(phone_re))

        pw_re = QtCore.QRegExp("[a-zA-Z0-9]{5,24}") # 비밀번호
        self.user_pass_lineEdit.setValidator(QtGui.QRegExpValidator(pw_re))
        self.pass_lineEdit.setValidator(QtGui.QRegExpValidator(pw_re))



        # 빠른 로그인
        self.user_phone_lineEdit.setText('01026723914')
        self.user_pass_lineEdit.setText('sansio2')

        # 빠른 회원가입
        self.phone_lineEdit.setText('01024353223')
        self.name_lineEdit.setText('테스트회원')
        self.pass_lineEdit.setText('2341')


    def initialize_socket(self):
        # ip = '127.0.0.1'
        ip = '10.10.21.122' # 컴퓨터 ip
        port = 9030
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))

    ## 서버에 DB 접근을 위한 데이터를 전달하는 함수들 @서버
    def login(self): #로그인 정보 전달
        '''
        GUI의 phone, pass 란에 입력한 전화번호와 비밀번호를 읽어와 서버에 전달한다.
        @서버:receive_message
        '''

        phone = self.user_phone_lineEdit.text()
        password = self.user_pass_lineEdit.text()

        if phone == '' or password == '':
            self.login_label.setText('휴대폰 번호와 비밀번호를 입력해주세요.')
            return

        # 서버에 전달하기 위한 딕셔너리 생성
        login = {'phone':phone, 'password':password}
        # 서버에 데이터를 전송하기 위한 send_data 함수 호출 (딕셔너리, 생성자)
        self.send_data(login, 'log')

    def check_phone(self): # 아이디 정보 전달
        '''
        GUI의 회원가입 란에서 입력한 전화번호를 읽어와 서버에 전달한다.
        @서버:receive_message
        '''
        print('아이디 중복확인')
        phone = self.phone_lineEdit.text()
        if phone != '':
            print('번호: ', phone)
            acount = {'phone': phone}
            self.send_data(acount, 'acc')
        else:
            print('아이디 비어있음')
            self.check_label.setText('휴대폰 번호를 입력해주세요.')

    def check_phone2(self):
        self.id_check = False
        self.check_label.setText('중복 확인을 눌러주세요.')

    def join(self): # 회원가입
        print('회원가입')
        if self.id_check == True:
            new_user = (self.name_lineEdit.text(), self.phone_lineEdit.text(), self.pass_lineEdit.text())
            msg = f"이름: {new_user[0]}\n휴대폰 번호: {new_user[1]}\n비밀번호: {new_user[2]}\n가입하시겠습니까?"

            # 가입 의사 확인 메시지박스
            reply = QMessageBox.question(self, '회원가입', msg,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 서버에 회원가입을 위한 데이터를 전달
                self.send_data(new_user, 'new') # 튜플 new_user, 식별자 'new'
                QMessageBox.information(self, '완료', '가입이 완료되었습니다.')
                print('가입 완료')

                # 회원가입 입력칸 초기화
                self.name_lineEdit.setText('')
                self.phone_lineEdit.setText('')
                self.pass_lineEdit.setText('')
                self.join_label.setText('')
                self.acount_tabWidget.setCurrentIndex(0)
                self.id_check = False

    def new_chatroom(self): # 새 채팅방 정보 전달
        '''
        GUI에서 채팅방 이름을 읽어와 서버에 전달한다.
        @서버:receive_message
        '''
        text = self.chat_name_line_edit.text()
        print(f'방제목: {text}')
        if text == '':
            return QMessageBox.information(self, '채팅 생성', '방 제목을 입력해주세요.')
        else:
            reply = QMessageBox.question(self, '채팅 생성', f"방장:'{self.user[0]}'\n'{text}' 채팅방을 생성하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                print(f'채팅방 [{text}] -- 생성 시도')
                # 서버로 방장의 계정(휴대폰 번호)과 방 제목을 포함한 딕셔너리를 전달
                new_room = {'master':self.user[1], 'title': text}
                self.send_data(new_room, 'cr0')


    def list_up_room(self): # 채팅 목록 조회 요청
        msg = 'cl1'
        self.client_socket.send(msg.encode())

    def chatroom(self): # 내용을 보려는 채팅방 정보 전달
        print('아직 작성 안함')



    ## 서버에 데이터를 전송하는 코드
    def send_data(self, data, idf:str): # 데이터를 전송하는 함수
        # DB에 넘겨줄 데이터를 포함하는 딕셔너리data와 식별자idf를 인자로 받음
        '''
        log : 로그인
        acc : 회원가입
        cl0 : 채팅방 생성
        cht : 채팅
        '''

        print('send_data -- ', end='')
        data = json.dumps(data) # 딕셔너리를 바이너리화 하는 json.dumps 메서드
        print('1', end='-')
        msg = idf + data # 식별자{딕셔너리내용}
        print('2', end='-')
        self.client_socket.send(msg.encode()) # 바이너리를 바이트로 바꿔서 전송
        print(f'{msg} 전송')

    def send_chat(self):
        # senders_name = self.user_name_line_edit_1p.text() #ui사용자이름
        senders_name = self.user[0] # 윗줄의 코드를 수정
        # print(1)
        data = self.signal_textEdit.toPlainText() #
        # print(2)
        self.receive_listWidget.addItem(f'{senders_name} : {data}') #ui
        # print(3)
        message = (f'{senders_name} : {data}').encode('utf-8')
        # print(4)
        self.client_socket.send(message)
        # print(5)
        self.signal_textEdit.clear()
        # print(6)

    # 서버의 응답을 받는 코드
    def receive_message(self, so):
        while True:
            buf = so.recv(9000)
            if not buf: # 연결종료
                break

            recv_data = buf.decode() # 서버에서 응답한 데이터를 decode
            print(recv_data)
            request = recv_data[0:3] # 서버의 응답에서 식별자 구분

            if len(recv_data) > 3: # 식별자 이외의 데이터가 존재한다면 데이터 할당
                self.last_request = recv_data[3:]

            else: # 없다면 None (서버에서의 DB 조회 결과가 None 인 경우)
                self.last_request = None

            if request != 'cht':
                if request == 'log': # 로그인
                    self.login_result()

                elif request == 'acc': # 중복확인
                    if self.last_request != None:  # 핸드폰 번호 조회 결과가 존재한다면
                        self.check_label.setText('이미 사용중인 번호입니다.')
                        self.id_check = False
                    else:
                        self.check_label.setText('사용 가능한 번호입니다.')
                        self.id_check = True
                # self.join_result()

                elif request == 'cl0': # 채팅생성
                    print('채팅방생성')

                elif request == 'cl1': # 채팅 목록 조회
                    print('채팅 조회')
                    print(self.last_request, '타입:', type(self.last_request))
                    if self.last_request != None:  # 핸드폰 번호 조회 결과가 존재한다면
                        print('채팅 목록')
                        temp = self.last_request
                        rooms = json.loads(temp)
                        self.chatroom_result(rooms)

            else: # 채팅
                print('채팅')
                self.receive_listWidget.addItem(f'{recv_data}')

        so.close()


    # 서버에서 응답한 데이터를 처리하는 코드
    def login_result(self): # 서버로부터 받은 응답으로 로그인 결과 실행
        if self.last_request != None:  # 핸드폰 번호 조회 결과가 존재한다면
            acount = json.loads(self.last_request)
            print(acount, '|', type(acount))
            name, id, pw = acount

            if self.user_pass_lineEdit.text() == pw:  # 비밀번호가 일치할 때
                print('phone / pass 일치, 로그인 확인')
                # self.user_name_label_2p.setText(self.user_name_line_edit_1p.text())
                self.user = acount
                self.stackedWidget.setCurrentIndex(1)  # 페이지 이동
                print('페이지이동', end='-')
                self.user_name_label_2p.setText(name)
                print('이름출력', end='-')
                self.list_up_room()  # 채팅방 목록 조회

                # 로그인 경고, 비밀번호 입력란 초기화
                self.login_label.setText('')
                self.user_pass_lineEdit.setText('')
            else:
                print('-- phone / pass 불일치')
                self.login_label.setText('비밀번호를 확인해주세요.')
        else:  # 조회된 계정이 존재하지 않을 때
            print('-- 조회된 계정 없음')
            self.login_label.setText('존재하지 않는 계정입니다.')
            return

    def chatroom_result(self, rooms): # 서버로부터 받은 응답으로 채팅방 생성 실행
        print('조회함수 들어옴')

        # QMessageBox.information(self, '완료', '채팅방이 생성되었습니다.')

        # 테이블 행 / 열 설정
        self.chat_list_tableWidget.setColumnCount(2)
        self.chat_list_tableWidget.setRowCount(len(rooms))

        col = 0
        for row in rooms:
            self.chat_list_tableWidget.setItem(col, 0, QTableWidgetItem(str(row[0])))
            self.chat_list_tableWidget.setItem(col, 1, QTableWidgetItem(str(row[1])))
            col += 1

            # 테이블 헤더 조정
            self.chat_list_tableWidget.setColumnWidth(0, 20)
            self.chat_list_tableWidget.horizontalHeader().setStretchLastSection(True)

        # 테이블 셀 클릭 이벤트
        self.chat_list_tableWidget.cellClicked.connect(self.select_chatroom)
        # # 이제 더블클릭 했을 때 채팅 내용 불러오기 하면 됨


        # 여기 오류
        self.chat_list_tableWidget.cellDoubleClicked.connect(self.chat_loads)


    def select_chatroom(self, row):
        r_num = self.chat_list_tableWidget.item(row, 0) # 방 번호
        r_name = self.chat_list_tableWidget.item(row, 1) # 방 이름

        room = (int(r_num.text()), r_name.text())
        print(f'@{room[0]}번 : {room[1]}')

    def chat_loads(self, row): # 채팅방 불러오기
        r_name = self.chat_list_tableWidget.item(row, 1) # 방 이름
        self.room_name_lable.setText(r_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    cThread.start()
    app.exec_()