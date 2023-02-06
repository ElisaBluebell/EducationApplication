import socket
import pymysql


class MainServer:
    def __init__(self):
        print(1)

    def socket_initialize(self):
        pass

    def send_data(self):
        pass


def execute_db(sql):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='educationapplication')
    c = conn.cursor()

    c.execute(sql)
    conn.commit()

    c.close()
    conn.close()


if __name__ == "__main__":
    main_server = MainServer
    main_server()
