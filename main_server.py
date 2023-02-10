import server_tool as st


class MainServer:
    def __init__(self):
        # xml_string = st.get_database_from_url('http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?serviceKey=yn8uwUR3eheqowtPnA9QRTQ9i8mYGhGEetp6HDG1hMhCeH9%2BNJFN6WlIM1AzfgrZB59syoKUT1rAVveE9J6Okg%3D%3D&searchMtNm=&searchArNm=&pageNo=1&numOfRows=100')
        # raw_data = st.xml_to_json(xml_string)

        # self.mntnm, self.aeatreason, self.overview, self.details = self.get_useful_data(raw_data)
        # st.null_to_zero([self.mntnm, self.aeatreason, self.overview, self.details])

        server_socket, socks = st.socket_initialize('10.10.21.121', 9000)
        st.turn_server_on(self.command_processor, server_socket, socks)

        # for i in range(len(self.mntnm)):
        #     print('length: ', len(self.mntnm))
        #     print('i + 1: ', i + 1)
        #     print('mntnm: ', self.mntnm[i])
        #     print('aeatreason: ', self.aeatreason[i])
        #     print('overview: ', self.overview[i])
        #     print('details: ', self.details[i])
        #     sql = f'''INSERT INTO education_data VALUES({i + 1}, "{self.mntnm[i]}", "{self.aeatreason[i]}", "{self.overview[i]}", "{self.details[i]}")'''
        #     st.execute_db(sql)

    def get_useful_data(self, raw_data):
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
            self.register_user(content, client_sock)

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


        # elif command == 'quiz_request':
        #     self.send_api_data_to_teacher(client_sock)

        elif command[:5] == '/quiz':
            self.send_quiz_by_location(command, client_sock)

    def student_login_process(self, login_list, client_sock):
        login_id, login_password = login_list
        if st.check_if_exist(login_id, 'user_account', 'user_id') == 0:
            st.send_command('/login_id_fail', '', client_sock)

        else:
            if st.check_if_exist(login_password, 'user_account', 'user_password') == 0:
                st.send_command('/login_password_fail', '', client_sock)

            else:
                quiz_table = st.get_whole_data('quiz')
                user_data = st.get_whole_data_where('user_account', 'user_id', login_id)
                login_data = [user_data, quiz_table]
                st.send_command('/login_success', login_data, client_sock)

    def teacher_login_process(self, login_list, client_sock):
        login_id, login_password = login_list
        if st.check_if_exist(login_id, 'user_account', 'user_id') == 0:
            st.send_command('/login_id_fail', '', client_sock)

        else:
            if st.check_if_exist(login_password, 'user_account', 'user_password') == 0:
                st.send_command('/login_password_fail', '', client_sock)

            else:
                login_name = st.get_single_item('user_name', 'user_account', 'user_id', login_id)
                st.send_command('/login_success', login_name, client_sock)

    def register_user(self, register_info, client_sock):
        user_class, user_name, user_id, user_password = register_info

        if st.check_if_exist(user_id, 'user_account', 'user_id') == 1:
            st.send_command('/register_fail', '', client_sock)

        else:
            self.regist_user(register_info, client_sock)

    def question_from_student(self, question_data, client_sock):
        posted_time, student_name, question = question_data
        print(posted_time)
        print(student_name)
        print(question)

        sql = f'INSERT INTO qna(posted_time, student_name, question) ' \
              f'VALUES("{posted_time}", "{student_name}", "{question}")'
        st.execute_db(sql)

        st.send_command('/post_success', '', client_sock)

    def send_whole_qna_data(self, dummy, client_sock):
        sql = 'SELECT * FROM qna'
        whole_qna = list(st.execute_db(sql))
        for i in range(len(whole_qna)):
            whole_qna[i] = list(whole_qna[i])
            for j in range(len(whole_qna[i])):
                if whole_qna[i][j] is None:
                    whole_qna[i][j] = 'X'
        st.send_command('/whole_qna_data', whole_qna, client_sock)

    def regist_user(self, register_info, client_sock):
        sql = f'INSERT INTO user_account (class, user_name, user_id, user_password, point)' \
              f' VALUES("{register_info[0]}", "{register_info[1]}", "{register_info[2]}", "{register_info[3]}", 0)'
        st.execute_db(sql)

        sql = 'CALL new_user()'
        st.execute_db(sql)

        st.send_command('/register_success', '', client_sock)

    def check_answer(self, answer, client_sock):
        sql = f'SELECT correct FROM quiz WHERE quiz_index={answer[0]}'
        correct_answer = st.execute_db(sql)[0][0]

    def insert_qna_answer_to_database(self, answer, client_sock):
        qna_index = answer[1]
        answer = answer[0]

        sql = f'UPDATE qna SET answer="{answer}" WHERE qna_index={qna_index}'
        st.execute_db(sql)

        st.send_command('/answer_submitted', '', client_sock)

    def send_quiz_by_location(self, location, client_sock):
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

        sql = f'SELECT quiz_index, question, correct, quiz_score FROM quiz WHERE area_name="{area_name}"'
        location_quiz = st.execute_db(sql)
        st.send_command('/location_quiz', location_quiz, client_sock)


if __name__ == "__main__":
    main_server = MainServer
    main_server()
