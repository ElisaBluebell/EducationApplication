import sys
from socket import *

from PyQt5.QtWidgets import QWidget, QApplication


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.set_socket()
        self.set_ui()

    def set_socket(self):
        ip = '10.10.21.121'  # 컴퓨터 ip
        port = 9000
        self.client_socket.connect((ip, port))

    def set_gui(self):
        self.setFixedHeight(800)
        self.setFixedWidth(600)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    app.exec_()
