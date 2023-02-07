import datetime
import requests
import xmltodict
import json
import pymysql
import socket


def socket_initialize():
    socks = []
    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('10.10.21.121', 9000))
    server_sock.listen()
    socks.append(server_sock)
    print(f' port {9000} is Waiting for Connection')
    return server_sock, socks


def add_client_to_socket_list(sock, socket_list):
    client_socket, addr = sock.accept()
    socket_list.append(client_socket)
    print(f'Client {client_socket.getpeername()} is Connected')
    return client_socket, addr, socket_list


def send_command(command, content, s):
    message = [command, content, s]
    data = json.dumps([command, content])
    print(f'Server Message: {data} [{datetime.datetime.now()}]')
    s.send(data.encode())


def connection_lost(sock, socks):
    print(f'Client {sock.getpeername()} Connection Lost')
    sock.close()
    socks.remove(sock)
    return socks


def get_database_from_url(url):
    response = requests.get(url)
    return response.text


def xml_to_json(xml_string):
    json_string = json.dumps(xmltodict.parse(xml_string), indent=4)
    return json.loads(json_string)


def get_useful_data(raw_data, i):
    return raw_data['response']['body']['items']['item'][i]['mntnm'], \
           raw_data['response']['body']['items']['item'][i]['aeatreason'], \
           raw_data['response']['body']['items']['item'][i]['overview'], \
           raw_data['response']['body']['items']['item'][i]['details']


def execute_db(sql):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='educationapplication')
    c = conn.cursor()

    c.execute(sql)
    conn.commit()

    c.close()
    conn.close()
