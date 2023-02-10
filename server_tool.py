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


def turn_server_on(command_processor, server_socket, socks):
    import datetime
    import select
    while True:
        read_socket, dummy1, dummy2 = select.select(socks, [], [], 0)
        for sock in read_socket:
            if sock == server_socket:
                client_socket, addr, socks = add_client_to_socket_list(sock, socks)

            else:
                try:
                    data = sock.recv(8192).decode('utf-8')
                    print(f'Received Data: {sock.getpeername()}: {data} [{datetime.datetime.now()}]')

                    if data:
                        try:
                            message = eval(data)
                            command_processor(message, sock)
                            print(f'Received Message: {sock.getpeername()}: {message} [{datetime.datetime.now()}]')

                        except TypeError:
                            print('TypeError Occurred')

                        except NameError:
                            print('NameError Occurred')

                    if not data:
                        socks = connection_lost(sock, socks)
                        continue

                except ConnectionResetError:
                    socks = connection_lost(sock, socks)
                    continue


def null_to_zero(item_list):
    for item in item_list:
        for i in range(len(item)):
            if item[i] is None:
                item[i] = 0


def check_if_exist(thing_need_check, table, column):
    sql = f'SELECT {column} FROM {table}'
    db_check_list = execute_db(sql)
    for i in range(len(db_check_list)):
        if thing_need_check == db_check_list[i][0]:
            return 1
    return 0


def get_single_item(item_column, table, column, key):
    sql = f'SELECT {item_column} FROM {table} WHERE {column}="{key}"'
    return execute_db(sql)[0][0]


def get_whole_data(table):
    sql = f'SELECT * FROM {table}'
    return execute_db(sql)


def get_whole_data_where(table, key_column, key):
    sql = f'SELECT * FROM {table} WHERE {key_column}="{key}"'
    return execute_db(sql)


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
