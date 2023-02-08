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


def get_single_item(key):
    sql = f'SELECT user_name FROM user_account WHERE user_id="{key}"'
    return execute_db(sql)[0][0]


def get_database_from_url(url):
    response = requests.get(url)
    return response.text


def xml_to_json(xml_string):
    json_string = json.dumps(xmltodict.parse(xml_string), indent=4)
    return json.loads(json_string)


def execute_db(sql):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='educationapplication')
    c = conn.cursor()

    c.execute(sql)
    conn.commit()

    return c.fetchall()
