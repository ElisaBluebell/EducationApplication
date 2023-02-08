import server_tool as st


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


def command_processor(message, client_sock):
    command = message[0]
    content = message[1]
    if command == '/register_user':
        register_user(content, client_sock)

    elif command == '/login_student':
        login_process(content, client_sock)

    elif command == '/login_teacher':
        login_process(content, client_sock)

    elif command == '/ask_student':
        question_from_student(content, client_sock)

    elif command == '/ask_check_student':
        send_whole_qna_data(content, client_sock)

    elif command == '/':
        pass


def login_process(login_list, client_sock):
    login_id, login_password = login_list
    if st.check_if_exist(login_id, 'user_account', 'user_id') == 0:
        st.send_command('/login_id_fail', '', client_sock)

    else:
        if st.check_if_exist(login_password, 'user_account', 'user_password') == 0:
            st.send_command('/login_password_fail', '', client_sock)

        else:
            login_name = st.get_single_item(login_id)
            st.send_command('/login_success', login_name, client_sock)


def register_user(register_info, client_sock):
    user_class, user_name, user_id, user_password = register_info

    if st.check_if_exist(user_id, 'user_account', 'user_id') == 1:
        st.send_command('/register_fail', '', client_sock)

    else:
        regist_user(register_info, client_sock)


def question_from_student(question_data, client_sock):
    posted_time, student_name, question = question_data
    print(posted_time)
    print(student_name)
    print(question)

    sql = f'INSERT INTO qna(posted_time, student_name, question) ' \
          f'VALUES("{posted_time}", "{student_name}", "{question}")'
    st.execute_db(sql)

    st.send_command('/post_success', '', client_sock)


def send_whole_qna_data(dummy, client_sock):
    sql = 'SELECT * FROM qna'
    whole_qna = list(st.execute_db(sql))
    for i in range(len(whole_qna)):
        whole_qna[i] = list(whole_qna[i])
        print(whole_qna)
        for j in range(len(whole_qna[i])):
            if whole_qna[i][j] is None:
                whole_qna[i][j] = 'X'
    st.send_command('/whole_qna_data', whole_qna, client_sock)


def regist_user(register_info, client_sock):
    sql = f'INSERT INTO user_account (class, user_name, user_id, user_password, point)' \
          f' VALUES("{register_info[0]}", "{register_info[1]}", "{register_info[2]}", "{register_info[3]}", 0)'
    st.execute_db(sql)

    sql = 'CALL new_user()'
    st.execute_db(sql)

    st.send_command('/register_success', '', client_sock)


def check_answer(self, answer, client_sock):
    sql = f'SELECT correct FROM quiz WHERE quiz_index={answer[0]}'
    correct_answer = st.execute_db(sql)[0][0]


def send_quiz_by_location(self, location, client_sock):
    pass
