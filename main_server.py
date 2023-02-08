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

                            except TypeError:
                                print('TypeError Occurred')

                        if not data:
                            self.socks = st.connection_lost(sock, self.socks)
                            continue

                    except ConnectionResetError:
                        self.socks = st.connection_lost(sock, self.socks)
                        continue

    @staticmethod
    def command_processor(message, client_sock):
        command = message[0]
        content = message[1]
        if command == '/register_user':
            st.register_user(content, client_sock)

        elif command == '/login_student':
            st.login_process(content, client_sock)

        elif command == '/login_teacher':
            st.login_process(content, client_sock)

        elif command == '/ask_student':
            st.question_from_student(content, client_sock)

        elif command == '/ask_check_student':
            st.send_whole_qna_data(content, client_sock)

        elif command == '/':
            pass

    def check_answer(self, answer, client_sock):
        sql = f'SELECT correct FROM quiz WHERE quiz_index={answer[0]}'
        correct_answer = st.execute_db(sql)[0][0]

    def send_quiz_by_location(self, location, client_sock):
        pass


if __name__ == "__main__":
    main_server = MainServer
    main_server()
