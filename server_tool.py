import datetime

import requests
import xmltodict
import json
import pymysql
import socket
import select


def socket_initialize(ip, port, socks):
    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen()
    socks.append(server_sock)
    return server_sock, socks


def turn_server_on(server_sock, sock_list, buffer):
    while True:
        r_sock, dummy1, dummy2 = select.select(sock_list, [], [], 0)
        for s in r_sock:
            if s == server_sock:
                print(s)
                c_sock, addr = s.accept()
                add_client_to_list(c_sock, addr, sock_list)

            else:
                try:
                    data = s.recv(buffer).decode('utf-8')
                    print(f'받은 메시지> {s.getpeername()}: {data} [{datetime.datetime.now()}]')

                    if data:
                        try:
                            message = eval(data)
                            print(message)
                            # data = json.dumps(['명령', '내용'])
                            # s.send(data.encode())

                        except TypeError:
                            data = json.dumps(['/load_chat_again', ''])
                            s.send(data.encode())

                    if not data:
                        print(f'클라이언트 {addr}이 접속을 종료했습니다.')
                        continue

                except ConnectionResetError:
                    print(f'클라이언트 {addr}이 접속을 종료했습니다.')
                    continue


def add_client_to_list(c_sock, addr, sock_list):
    sock_list.append(c_sock)
    print(f'클라이언트 {addr}가 접속했습니다.')


def get_database_from_url(url):
    response = requests.get(url)
    return response.text


def xml_to_json(xml_string):
    json_string = json.dumps(xmltodict.parse(xml_string), indent=4)
    return json.loads(json_string)


def get_useful_data(raw_data, i):
    return raw_data['response']['body']['items']['item'][i]['mntnm'], \
           raw_data['response']['body']['items']['item'][i]['mntheight'], \
           raw_data['response']['body']['items']['item'][i]['aeatreason'], \
           raw_data['response']['body']['items']['item'][i]['overview'], \
           raw_data['response']['body']['items']['item'][i]['details'], \
           raw_data['response']['body']['items']['item'][i]['transport'], \
           raw_data['response']['body']['items']['item'][i]['tourisminf'], \
           raw_data['response']['body']['items']['item'][i]['etccourse']


def execute_db(sql):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='educationapplication')
    c = conn.cursor()

    c.execute(sql)
    conn.commit()

    c.close()
    conn.close()
