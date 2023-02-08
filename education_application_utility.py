import server_tool as st


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
