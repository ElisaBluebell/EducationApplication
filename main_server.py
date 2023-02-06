import server_tool as st
import select


class MainServer:
    def __init__(self):
        buffer = 1024
        server_sock, socks = st.socket_initialize()

        xml_string = st.get_database_from_url(
            'http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?'
            'serviceKey=yn8uwUR3eheqowtPnA9QRTQ9i8mYGhGEetp6HDG1hMhCeH9%2BNJFN6WlIM1AzfgrZB59syoKUT1rAVveE9J6Okg%3D%3D&'
            'searchMtNm=&'
            'searchArNm=&'
            'pageNo=1&'
            'numOfRows=100')

        json_dict = st.xml_to_json(xml_string)
        body = st.get_useful_data(json_dict, 1)
        print(body)

        self.turn_server_on(server_sock, socks, buffer)

    def turn_server_on(self, server_sock, sock_list, buffer):
        import datetime
        import json
        while True:
            r_sock, dummy1, dummy2 = select.select(sock_list, [], [], 0)
            for s in r_sock:
                if s == server_sock:
                    print(s)
                    c_sock, addr = s.accept()
                    st.add_client_to_list(c_sock, addr, sock_list)

                else:
                    try:
                        data = s.recv(buffer).decode('utf-8')
                        print(f'받은 메시지> {s.getpeername()}: {data} [{datetime.datetime.now()}]')

                        if data:
                            try:
                                message = eval(data)
                                return message
                                # data = json.dumps(['명령', '내용'])
                                # s.send(data.encode())

                            except TypeError:
                                data = json.dumps(['/load_chat_again', ''])
                                s.send(data.encode())

                        if not data:
                            print(f'클라이언트 {addr}이 접속을 종료했습니다.')
                            s.close()
                            continue

                    except ConnectionResetError:
                        print(f'클라이언트 {addr}이 접속을 종료했습니다.')
                        s.close()
                        continue


if __name__ == "__main__":
    main_server = MainServer
    main_server()
