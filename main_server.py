import datetime

import select
import server_tool as st


class MainServer:
    def __init__(self):
        xml_string = st.get_database_from_url('http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?serviceKey=yn8uwUR3eheqowtPnA9QRTQ9i8mYGhGEetp6HDG1hMhCeH9%2BNJFN6WlIM1AzfgrZB59syoKUT1rAVveE9J6Okg%3D%3D&searchMtNm=&searchArNm=&pageNo=1&numOfRows=100')
        raw_data = st.xml_to_json(xml_string)
        mntnm, aeatreason, overview, details = st.get_useful_data(raw_data)
        self.server_socket, self.socks = st.socket_initialize('10.10.21.121', 9000)
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
        if command == '/register_user':
            self.register_user(content, client_sock)

        elif command == '/login_student':
            self.student_login(content, client_sock)

        elif command == '/ask_student':
            self.question_from_student(content, client_sock)

    def register_user(self, register_info, client_sock):
        user_class, user_name, user_id, user_password = register_info

        if self.check_if_exist(user_id, 'account', 'user_id') == 1:
            st.send_command('/register_fail', '', client_sock)

        else:
            self.regist_user(register_info, client_sock)

    def check_if_exist(self, thing_need_check, table, column):
        sql = f'SELECT {column} FROM {table}'
        db_check_list = st.execute_db(sql)
        for i in range(len(db_check_list)):
            if thing_need_check == db_check_list[i][0]:
                return 1
        return 0

    def regist_user(self, register_info, client_sock):
        sql = f'INSERT INTO account VALUES("{register_info[0]}", "{register_info[1]}", "{register_info[2]}", ' \
              f'"{register_info[3]}")'
        st.execute_db(sql)
        st.send_command('/register_success', '', client_sock)

    def student_login(self, login_list, client_sock):
        login_id, login_password = login_list
        if self.check_if_exist(login_id, 'account', 'user_id') == 0:
            st.send_command('/login_id_fail', '', client_sock)

        else:
            if self.check_if_exist(login_password, 'account', 'user_password') == 0:
                st.send_command('/login_password_fail', '', client_sock)

            else:
                login_name = self.get_user_name(login_id)
                st.send_command('/login_success', login_name, client_sock)

    def get_user_name(self, user_id):
        sql = f'SELECT user_name FROM account WHERE user_id="{user_id}"'
        return st.execute_db(sql)[0][0]

    def question_from_student(self, question_data, client_sock):
        posted_time, student_name, question = question_data
        print(posted_time)
        print(student_name)
        print(question)

        sql = f'INSERT INTO qna(posted_time, student_name, question) ' \
              f'VALUES("{posted_time}", "{student_name}", "{question}")'
        st.execute_db(sql)

        st.send_command('/post_success', '', client_sock)


if __name__ == "__main__":
    main_server = MainServer
    main_server()
