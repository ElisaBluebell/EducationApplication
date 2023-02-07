import datetime
import select
import server_tool as st


class MainServer:
    def __init__(self):
        self.server_socket, self.socks = st.socket_initialize()
        self.turn_server_on()

    def turn_server_on(self):
        while True:
            read_socket, dummy1, dummy2 = select.select(self.socks, [], [], 0)
            for sock in read_socket:
                if sock == self.server_socket:
                    client_socket, addr, self.socks = st.add_client_to_socket_list(sock, self.socks)

                else:
                    try:
                        data = sock.recv(1024).decode('utf-8')
                        print(f'Received Message: {sock.getpeername()}: {data} [{datetime.datetime.now()}]')

                        if data:
                            try:
                                message = eval(data)
                                self.command_processor(message, sock)
                                st.send_command('/This is Server', '', sock)

                            except TypeError:
                                print('TypeError Occurred')

                        if not data:
                            self.socks = st.connection_lost(sock, self.socks)
                            continue

                    except ConnectionResetError:
                        self.socks = st.connection_lost(sock, self.socks)
                        continue


    @staticmethod
    def command_processor(message, client_sock):
        command = message[0]
        content = message[1]


if __name__ == "__main__":
    main_server = MainServer
    main_server()
