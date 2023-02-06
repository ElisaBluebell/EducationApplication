import datetime
import json
import socket

import server_tool as st
import select


class MainServer:
    def __init__(self):
        self.socks = []
        self.s_sock = socket.socket()
        self.ip = '10.10.21.121'
        self.port = 9000
        self.initialize_socket()
        self.turn_server_on()

    # 소켓 설정 함수
    def initialize_socket(self):
        self.s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        self.s_sock.listen()
        self.socks.append(self.s_sock)
        print(f'{self.port} 포트 열림')

    def turn_server_on(self):
        while True:
            r_sock, dummy1, dummy2 = select.select(self.socks, [], [], 0)
            for s in r_sock:
                if s == self.s_sock:
                    c_sock, addr = s.accept()
                    self.socks.append(c_sock)
                    print(f'{c_sock.getpeername()} 접속')

                else:
                    try:
                        data = s.recv(1024).decode('utf-8')
                        print(f'받은 메시지: {s.getpeername()}: {data} [{datetime.datetime.now()}]')

                        if data:
                            try:
                                message = eval(data)
                                self.command_processor(message, s)

                            except TypeError:
                                data = json.dumps(['/load_chat_again', ''])
                                s.send(data.encode())

                        if not data:
                            self.connection_lost(s)
                            continue

                    except ConnectionResetError:
                        self.connection_lost(s)
                        continue

    def connection_lost(self, s):
        print(f'{s.getpeername()} 접속 종료')
        s.close()
        self.socks.remove(s)

    @staticmethod
    def command_processor(message, client_sock):
        command = message[0]
        content = message[1]
        pass

    def send_command(self, command, content, s):
        message = [command, content, s]
        data = json.dumps([command, content])
        print(f'보낸 메시지: {data} [{datetime.datetime.now()}]')
        s.send(data.encode())


if __name__ == "__main__":
    main_server = MainServer
    main_server()
