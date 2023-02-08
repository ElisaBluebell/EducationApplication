import datetime
import requests
import xmltodict
import json
import pymysql
import socket


def socket_initialize(ip, port):
    socks = []
    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen()
    socks.append(server_sock)
    print(f' port {port} is Waiting for Connection')
    return server_sock, socks


def add_client_to_socket_list(sock, socket_list):
    client_socket, addr = sock.accept()
    socket_list.append(client_socket)
    print(f'Client {client_socket.getpeername()} is Connected')
    return client_socket, addr, socket_list


def send_command(command, content, s):
    print(f'Server Message: {command}, {content} [{datetime.datetime.now()}]')
    data = json.dumps([command, content])
    s.send(data.encode())


def connection_lost(sock, socks):
    print(f'Client {sock.getpeername()} Connection Lost')
    sock.close()
    socks.remove(sock)
    return socks


def check_if_exist(thing_need_check, table, column):
    sql = f'SELECT {column} FROM {table}'
    db_check_list = execute_db(sql)
    for i in range(len(db_check_list)):
        if thing_need_check == db_check_list[i][0]:
            return 1
    return 0


def login_process(login_list, client_sock):
    login_id, login_password = login_list
    if check_if_exist(login_id, 'user_account', 'user_id') == 0:
        send_command('/login_id_fail', '', client_sock)

    else:
        if check_if_exist(login_password, 'user_account', 'user_password') == 0:
            send_command('/login_password_fail', '', client_sock)

        else:
            login_name = get_user_name(login_id)
            send_command('/login_success', login_name, client_sock)


def get_user_name(user_id):
    sql = f'SELECT user_name FROM user_account WHERE user_id="{user_id}"'
    return execute_db(sql)[0][0]


def register_user(register_info, client_sock):
    user_class, user_name, user_id, user_password = register_info

    if check_if_exist(user_id, 'user_account', 'user_id') == 1:
        send_command('/register_fail', '', client_sock)

    else:
        regist_user(register_info, client_sock)


def question_from_student(question_data, client_sock):
    posted_time, student_name, question = question_data
    print(posted_time)
    print(student_name)
    print(question)

    sql = f'INSERT INTO qna(posted_time, student_name, question) ' \
          f'VALUES("{posted_time}", "{student_name}", "{question}")'
    execute_db(sql)

    send_command('/post_success', '', client_sock)


def send_whole_qna_data(dummy, client_sock):
    sql = 'SELECT * FROM qna'
    whole_qna = list(execute_db(sql))
    for i in range(len(whole_qna)):
        whole_qna[i] = list(whole_qna[i])
        print(whole_qna)
        for j in range(len(whole_qna[i])):
            if whole_qna[i][j] is None:
                whole_qna[i][j] = 'X'
    send_command('/whole_qna_data', whole_qna, client_sock)


def regist_user(register_info, client_sock):
    sql = f'INSERT INTO user_account (class, user_name, user_id, user_password, point)' \
          f' VALUES("{register_info[0]}", "{register_info[1]}", "{register_info[2]}", "{register_info[3]}", 0)'
    execute_db(sql)

    sql = 'CALL new_user()'
    execute_db(sql)

    send_command('/register_success', '', client_sock)


def get_database_from_url(url):
    response = requests.get(url)
    return response.text


def xml_to_json(xml_string):
    json_string = json.dumps(xmltodict.parse(xml_string), indent=4)
    return json.loads(json_string)


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


def execute_db(sql):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='educationapplication')
    c = conn.cursor()

    c.execute(sql)
    conn.commit()

    return c.fetchall()
