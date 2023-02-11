import server_tool as st

login_student_index_socket = {}
login_teacher_index_socket = {}


class MainServer:
    def __init__(self):
        server_socket, socks = st.socket_initialize('10.10.21.121', 9000)
        self.turn_server_on(self.command_processor, server_socket, socks)

    def turn_server_on(self, command_processor, server_socket, socks):
        import datetime
        import select
        while True:
            read_socket, dummy1, dummy2 = select.select(socks, [], [], 0)
            for sock in read_socket:
                if sock == server_socket:
                    client_socket, addr, socks = st.add_client_to_socket_list(sock, socks)

                else:
                    try:
                        data = sock.recv(8192).decode('utf-8')
                        print(f'Received Data: {sock.getpeername()}: {data} [{datetime.datetime.now()}]')

                        if data:
                            try:
                                message = eval(data)
                                command_processor(message, sock)
                                print(f'Received Message: {sock.getpeername()}: {message} [{datetime.datetime.now()}]')

                            # except TypeError:
                            #     print('TypeError Occurred')

                            except NameError:
                                print('NameError Occurred')

                            # except:
                            #     print('에러 발생')

                        if not data:
                            socks = self.connection_lost(sock, socks)
                            continue

                    except ConnectionResetError:
                        socks = self.connection_lost(sock, socks)
                        continue

                    # except:
                    #     print('에러 발생')

    @staticmethod
    def connection_lost(sock, socks):
        print(f'Client {sock.getpeername()} Connection Lost')

        for i in login_student_index_socket.keys():
            if login_student_index_socket[i] == sock:
                del login_student_index_socket[i]
                break

        if login_student_index_socket:
            print('login_student: ', login_student_index_socket)

        for i in login_teacher_index_socket.keys():
            if login_teacher_index_socket[i] == sock:
                del login_teacher_index_socket[i]
                break

        if login_teacher_index_socket:
            print('login_teacher: ', login_teacher_index_socket)

        sock.close()
        socks.remove(sock)
        return socks

    @staticmethod
    def get_useful_data(raw_data):
        mntnm = []
        aeatreason = []
        overview = []
        details = []
        for i in range(len(raw_data['response']['body']['items']['item'])):
            mntnm.append(raw_data['response']['body']['items']['item'][i]['mntnm'])
            aeatreason.append(raw_data['response']['body']['items']['item'][i]['aeatreason'])
            overview.append(raw_data['response']['body']['items']['item'][i]['overview'])
            details.append(raw_data['response']['body']['items']['item'][i]['details'])
        return mntnm, aeatreason, overview, details

    def command_processor(self, message, client_sock):
        command = message[0]
        content = message[1]
        if command == '/register_user':
            self.check_registrable(content, client_sock)

        elif command == '/login_student':
            self.student_login_process(content, client_sock)

        elif command == '/login_teacher':
            self.teacher_login_process(content, client_sock)

        elif command == '/ask_student':
            self.question_from_student(content, client_sock)

        elif command == '/ask_check_student':
            self.send_whole_qna_data(content, client_sock)

        elif command == '/qna':
            self.send_whole_qna_data(content, client_sock)

        elif command == '/answer_send':
            self.insert_qna_answer_to_database(content, client_sock)

        elif command == '/student_score':
            self.student_score(client_sock)

        elif command == '/update_send':
            self.add_quiz(content, client_sock)

        elif command == '/temp_recieve_chat':
            self.receive_chat_message(content)

        elif command == '/temp_send_chat':
            self.send_chat_message(content, client_sock)

        elif command == '/student_chat':
            self.student_chat_message(content, client_sock)

        elif command == '/save_learning_user':
            self.insert_score(content, client_sock)

        elif command == '/request_login_member_list':
            self.send_login_member_list(client_sock)

        elif command == '/load_learning_user':
            self.load_learning_user(client_sock)

        elif command[:5] == '/quiz':
            self.send_quiz_by_location(command, client_sock)

        else:
            pass

    def check_registrable(self, regist_info, client_sock):
        user_class, user_name, user_id, user_password = regist_info

        if st.check_if_item_exist(user_id, 'user_account', 'user_id') == 1:
            st.send_command('/register_fail', '', client_sock)

        else:
            self.regist_user(regist_info, client_sock)

    @staticmethod
    def regist_user(register_info, client_sock):
        sql = f'INSERT INTO user_account (class, user_name, user_id, user_password, point)' \
              f' VALUES("{register_info[0]}", "{register_info[1]}", "{register_info[2]}", "{register_info[3]}", 0);'
        st.execute_db(sql)

        sql = 'CALL new_user()'
        st.execute_db(sql)

        st.send_command('/register_success', '', client_sock)

    @staticmethod
    def student_login_process(login_list, client_sock):
        login_id, login_password = login_list
        if st.check_if_item_exist(login_id, 'user_account', 'user_id') == 0:
            st.send_command('/login_id_fail', '', client_sock)

        else:
            if st.check_if_item_exist(login_password, 'user_account', 'user_password') == 0:
                st.send_command('/login_password_fail', '', client_sock)

            else:
                quiz_table = st.get_whole_data('quiz')
                user_data = st.get_whole_data_where('user_account', 'user_id', login_id)
                login_data = [user_data, quiz_table]
                login_student_index_socket[user_data[0][0]] = client_sock
                print('login_student: ', login_student_index_socket)
                st.send_command('/login_success', login_data, client_sock)

    @staticmethod
    def teacher_login_process(login_list, client_sock):
        login_id, login_password = login_list
        if st.check_if_item_exist(login_id, 'user_account', 'user_id') == 0:
            st.send_command('/login_id_fail', '', client_sock)

        else:
            if st.check_if_item_exist(login_password, 'user_account', 'user_password') == 0:
                st.send_command('/login_password_fail', '', client_sock)

            else:
                user_data = st.get_whole_data_where('user_account', 'user_id', login_id)
                login_name = st.get_single_item('user_name', 'user_account', 'user_id', login_id)
                login_teacher_index_socket[user_data[0][0]] = client_sock
                print('login_teacher: ', login_teacher_index_socket)
                st.send_command('/login_success', login_name, client_sock)

    @staticmethod
    def question_from_student(question_data, client_sock):
        posted_time, student_name, question = question_data

        sql = f'INSERT INTO qna(posted_time, student_name, question) ' \
              f'VALUES("{posted_time}", "{student_name}", "{question}");'
        st.execute_db(sql)

        st.send_command('/post_success', '', client_sock)

    @staticmethod
    def send_whole_qna_data(dummy, client_sock):
        sql = 'SELECT * FROM qna'
        whole_qna = list(st.execute_db(sql))
        for i in range(len(whole_qna)):
            whole_qna[i] = list(whole_qna[i])
            for j in range(len(whole_qna[i])):
                if whole_qna[i][j] is None:
                    whole_qna[i][j] = 'X'
        st.send_command('/whole_qna_data', whole_qna, client_sock)

    @staticmethod
    def insert_score(answer, client_sock):
        for i in range(1, len(answer)):
            if answer[i][1] == 'O':
                sql = f'UPDATE score_board SET correct="{answer[i][2]}", solve_datetime="{answer[i][3]}" WHERE user_index={answer[0]} and quiz_index={answer[i][0]};'

            else:
                sql = f'UPDATE score_board SET correct="{answer[i][1]}", solve_datetime="{answer[i][3]}" WHERE user_index={answer[0]} and quiz_index={answer[i][0]};'
            st.execute_db(sql)

        st.send_command('/score_board_updated', '', client_sock)

    @staticmethod
    def insert_qna_answer_to_database(answer, client_sock):
        qna_index = answer[1]
        answer = answer[0]

        sql = f'UPDATE qna SET answer="{answer}" WHERE qna_index={qna_index};'
        st.execute_db(sql)

        st.send_command('/answer_submitted', '', client_sock)

    @staticmethod
    def student_score(client_sock):
        user_index = []
        user_score_data = []

        sql = 'SELECT user_index FROM user_account WHERE class="학생";'
        user_number = st.execute_db(sql)

        for i in range(len(user_number)):
            user_index.append(user_number[i][0])

        for i in user_index:
            sql = f'SELECT user_name FROM user_account WHERE user_index={i};'
            user_name = st.execute_db(sql)[0][0]

            sql = f'''
            SELECT SUM(a.correct), 
            SUM(a.solve_datetime), 
            b.area_name 
            FROM score_board AS a 
            INNER JOIN quiz AS b 
            ON a.quiz_index=b.quiz_index 
            WHERE a.user_index={i} 
            GROUP BY b.area_name
            ;'''
            user_score = st.execute_db(sql)
            user_score = list(user_score)
            for j in range(len(user_score)):
                user_score[j] = list(user_score[j])

            st.null_to_zero(user_score)
            user_data = [user_name, user_score]

            user_score_data.append(user_data)

        st.send_command('/student_score', user_score_data, client_sock)

    @staticmethod
    def add_quiz(data, client_sock):
        quiz = data[0]
        answer = data[1]
        area_name = data[2][1:-4]

        if area_name == 'gangwon':
            area_name = '강원도'
        elif area_name == 'seoul':
            area_name = '서울/경기'
        elif area_name == 'chungbuk':
            area_name = '충청북도'
        elif area_name == 'chungnam':
            area_name = '충청남도'
        elif area_name == 'gyeongbuk':
            area_name = '경상북도'
        elif area_name == 'gyeongnam':
            area_name = '경상남도'
        elif area_name == 'jeonbuk':
            area_name = '전라북도'
        elif area_name == 'jeonnam':
            area_name = '전라남도'
        else:
            area_name = '제주도'

        sql = f'INSERT INTO quiz(question, correct, area_name, quiz_score) ' \
              f'VALUES("{quiz}", "{answer}", "{area_name}", 10);'
        st.execute_db(sql)

        sql = 'CALL new_quiz()'
        st.execute_db(sql)

        st.send_command('/quiz_inserted', '', client_sock)

    @staticmethod
    def send_quiz_by_location(location, client_sock):
        location = location[7:]
        if location == 'gangwon':
            area_name = '강원도'
        elif location == 'seoul':
            area_name = '서울/경기'
        elif location == 'chungbuk':
            area_name = '충청북도'
        elif location == 'chungnam':
            area_name = '충청남도'
        elif location == 'gyeongbuk':
            area_name = '경상북도'
        elif location == 'gyeongnam':
            area_name = '경상남도'
        elif location == 'jeonbuk':
            area_name = '전라북도'
        elif location == 'jeonnam':
            area_name = '전라남도'
        else:
            area_name = '제주도'

        sql = f'SELECT quiz_index, question, correct, quiz_score FROM quiz WHERE area_name="{area_name}";'
        location_quiz = st.execute_db(sql)
        st.send_command('/location_quiz', location_quiz, client_sock)

    def send_login_member_list(self, client_sock):
        user_list = []
        for i in login_teacher_index_socket.keys():
            if login_teacher_index_socket[i] == client_sock:
                for j in login_student_index_socket.keys():
                    user_list.append(j)
                self.get_user_name(user_list, client_sock)

        for i in login_student_index_socket.keys():
            if login_student_index_socket[i] == client_sock:
                for j in login_teacher_index_socket.keys():
                    user_list.append(j)
                self.get_user_name(user_list, client_sock)

    def get_user_name(self, user_index_list, client_sock):
        user_name_list = []
        for i in range(len(user_index_list)):
            sql = f'SELECT user_name FROM user_account WHERE user_index={user_index_list[i]}'
            user_name_list.append(st.execute_db(sql)[0][0])
        st.send_command('/get_user_name', user_name_list, client_sock)

    def get_user_index(self, client_sock):
        for i in login_student_index_socket.keys():
            if login_student_index_socket[i] == client_sock:
                return i

    def load_learning_user(self, client_sock):
        student = self.get_user_index(client_sock)

        sql = f'SELECT a.quiz_index, b.area_name ' \
              f'FROM score_board AS a ' \
              f'INNER JOIN quiz AS b ' \
              f'ON a.quiz_index=b.quiz_index ' \
              f'WHERE a.solve_datetime is null ' \
              f'AND a.user_index={student}'
        learning_progress = st.execute_db(sql)

        st.send_command('/learning_progress', learning_progress, client_sock)

    # def check_requester_class(self, client_sock):

    #
    # def get_login_student_list(self, client_sock):
    #     sql = 'SELECT user_index FROM user_account WHERE class="학생"'
    #     student_list = st.execute_db(sql)
    #     print(student_list)
    #
    #
    # def get_login_teacher_list(self, client_sock):
    #     sql = 'SELECT user_index FROM user_account WHERE class="교사"'
    #     teacher_list = st.execute_db(sql)
    #     print(teacher_list)

    def receive_chat_message(self, content):
        pass

    def student_chat_message(self, content, client_sock):
        pass

    def send_chat_message(self, content, client_sock):
        pass


if __name__ == "__main__":
    main_server = MainServer
    main_server()
