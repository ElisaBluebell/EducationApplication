import sys
import threading
import server_tool as st
from socket import *

from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QHeaderView, QListWidget, QLineEdit, QComboBox, \
    QPushButton


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.set_socket()
        self.login_process()
        self.set_gui()

        cThread = threading.Thread(target=self.receive_message, args=(self.client_socket,), daemon=True)
        cThread.start()

    def set_socket(self):
        ip = '10.10.21.121'  # 컴퓨터 ip
        port = 9000
        self.client_socket.connect((ip, port))

    def set_gui(self):
        self.setFixedHeight(800)
        self.setFixedWidth(600)
        self.show()
        self.chat_client()

    def login_process(self):
        login_data = ['ElisaBluebell', '1234']
        st.send_command('/login_teacher', login_data, self.client_socket)
        # pass

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

            else:
                pass

    def chat_client(self):
        st.send_command('/request_login_member_list', '', self.client_socket)

        self.member_select = QComboBox(self)
        self.member_select.setGeometry(20, 20, 160, 20)
        self.show_chat_opponent_list()

        self.chat_window = QListWidget(self)
        self.chat_window.setGeometry(20, 120, 560, 560)

        self.input_chat = QLineEdit(self)
        self.input_chat.setGeometry(20, 700, 500, 20)
        self.input_chat.returnPressed.connect(self.send_chat)

        self.send = QPushButton(self)
        self.send.setGeometry(540, 700, 40, 20)
        self.send.setText('전송')
        self.send.clicked.connect(self.send_chat)

    def show_chat_opponent_list(self):
        pass

    def renew_user_list(self, content):
        self.login_user = {}
        # self.login_user.

    def send_chat(self):
        self.input_chat.clear()

    def receive_chat(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    app.exec_()
