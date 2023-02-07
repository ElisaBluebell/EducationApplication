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
