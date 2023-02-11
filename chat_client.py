import sys
import threading
import time

import server_tool as st
from socket import *

from PyQt5.QtWidgets import QWidget, QApplication,QListWidget, QLineEdit, QComboBox, QPushButton


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.set_socket()
        # 채팅 가능 여부 판별용 스위치
        self.chat_able = 0
        cThread = threading.Thread(target=self.receive_message, args=(self.client_socket,), daemon=True)
        cThread.start()

        self.login_process()
        self.set_gui()

    def set_socket(self):
        ip = '10.10.21.121'  # 컴퓨터 ip
        port = 9000
        self.client_socket.connect((ip, port))

    def set_gui(self):
        self.setFixedHeight(800)
        self.setFixedWidth(600)
        self.chat_client()
        self.show()

    def login_process(self):
        login_data = ['ElisaBluebell', '1234']
        st.send_command('/login_teacher', login_data, self.client_socket)

    def receive_message(self, so):
        while True:
            buf = so.recv(8192)
            if not buf:  # 연결종료
                break

            recv_data = buf.decode()  # 서버에서 응답한 데이터를 decode
            print(recv_data)
            request = eval(recv_data)  # 서버의 응답에서 식별자 구분
            command = request[0]
            content = request[1]
            print(f'command: {command}')
            print(f'content: {content}')

            if content == '':
                pass

            elif command == '/login_user_list':
                self.renew_user_list(content)

            elif command == '/reseive_chat':
                self.receive_chat()

            # 현재 접속중인 유저명 저장, 학생 로그인의 경우 user_name 재설정 필요
            elif command == '/login_success':
                self.user_name = content

            elif command == '/get_user_name':
                self.renew_user_list(content)

            elif command == '/get_past_chat':
                self.print_past_chat(content)

            else:
                pass

    def chat_client(self):
        self.user_select = QComboBox(self)
        self.user_select.setGeometry(20, 20, 200, 20)
        self.user_select.currentTextChanged.connect(self.request_past_chat_data)

        self.chat_window = QListWidget(self)
        self.chat_window.setGeometry(20, 120, 560, 560)

        self.input_chat = QLineEdit(self)
        self.input_chat.setGeometry(20, 700, 500, 20)
        self.input_chat.returnPressed.connect(self.send_chat)

        self.send = QPushButton(self)
        self.send.setGeometry(540, 700, 40, 20)
        self.send.setText('전송')
        self.send.clicked.connect(self.send_chat)

        st.send_command('/request_login_member_list', '', self.client_socket)

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
        st.send_command('/request_past_chat_data', [self.user_name, self.user_select.currentText()], self.client_socket)
        # print('유저명: ', self.user_select.currentText())

    # 지난 채팅 출력 기능
    def print_past_chat(self, past_chat):
        # 서버로부터 받아온 지난 채팅 리스트의 길이만큼 반복해서 출력
        for i in range(len(past_chat)):
            self.chat_window.addItem(past_chat[i])

        # 이후 스크롤 바닥으로
        time.sleep(0.01)
        self.chat_window.scrollToBottom()

    # 채팅 전송 기능
    def send_chat(self):
        chat_to_send = self.input_chat.text()
        # 채팅창 초기화
        self.input_chat.clear()

        chat_data = [self.user_name, self.user_select.currentText(), chat_to_send]
        st.send_command('/new_chat', chat_data, self.client_socket)

    def receive_chat(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    app.exec_()
