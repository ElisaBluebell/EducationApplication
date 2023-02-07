import datetime
import json

import select
import server_tool as st


class MainServer:
    def __init__(self):
        self.server_socket, self.socks = st.socket_initialize()
        self.turn_server_on()

    def turn_server_on(self):
        while True:
            read_socket, dummy1, dummy2 = select.select(self.socks, [], [], 0)
            for sock in read_socket:
                if sock == self.server_socket:
                    client_socket, addr, self.socks = st.add_client_to_socket_list(sock, self.socks)

                else:
                    try:
                        data = sock.recv(1024).decode('utf-8')
                        print(f'Received Message: {sock.getpeername()}: {data} [{datetime.datetime.now()}]')

                        if data:
                            try:
                                message = eval(data)
                                self.command_processor(message, sock)
                                # st.send_command('/This is Server', '', sock)

                            except TypeError:
                                print('TypeError Occurred')

                        if not data:
                            self.socks = st.connection_lost(sock, self.socks)
                            continue

                    except ConnectionResetError:
                        self.socks = st.connection_lost(sock, self.socks)
                        continue

    def command_processor(self, message, client_sock):
        print(message)
        command = message[0]
        content = message[1]
        if command == '/register_student':
            self.register_student(content, client_sock)

    def register_student(self, register_info, client_sock):

        user_class, user_name, user_id, user_password = register_info

        if self.check_if_overlapped(user_id) == 1:
            st.send_command('/register_fail', '', client_sock)

        else:
            self.regist_user(register_info, client_sock)

    def check_if_overlapped(self, user_id):
        sql = 'SELECT user_id FROM account'
        db_user_id = st.execute_db(sql)
        for i in range(len(db_user_id)):
            if user_id == db_user_id[i][0]:
                return 1
        return 0

    def regist_user(self, register_info, client_sock):
        sql = f'INSERT INTO account VALUES("{register_info[0]}", "{register_info[1]}", "{register_info[2]}", ' \
              f'"{register_info[3]}")'
        st.execute_db(sql)

        st.send_command('/register_success', '', client_sock)


if __name__ == "__main__":
    main_server = MainServer
    main_server()
