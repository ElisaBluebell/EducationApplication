import sys
import threading
import server_tool as st
from socket import *

from PyQt5.QtWidgets import QWidget, QApplication,QListWidget, QLineEdit, QComboBox, QPushButton


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.set_socket()
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

    def renew_user_list(self, content):
        self.user_select.clear()
        connectable_user_list = content

        if connectable_user_list:
            self.chat_able = 1
            for connectable_user in connectable_user_list:
                self.user_select.addItem(connectable_user)

        else:
            self.user_select.addItem('지금은 상담이 불가능합니다.')
            self.chat_able = 0

    def request_past_chat_data(self):
        # if self.chat_able == 1:
        st.send_command('/request_past_chat_data', [self.user_name, self.user_select.currentText()], self.client_socket)
        # print('유저명: ', self.user_select.currentText())

    def print_past_chat(self):
        pass

    def send_chat(self):
        self.input_chat.clear()

    def receive_chat(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    app.exec_()
