import socket
import server_tool as sm


class MainServer:
    def __init__(self):
        buffer = 1024
        self.get_api_data()
        server_sock, socks = sm.socket_initialize()
        print(server_sock.getsockname())
        sm.turn_server_on(server_sock, socks, buffer)


    @staticmethod
    def get_api_data():
        xml_string = sm.get_database_from_url(
            'http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?'
            'serviceKey=yn8uwUR3eheqowtPnA9QRTQ9i8mYGhGEetp6HDG1hMhCeH9%2BNJFN6WlIM1AzfgrZB59syoKUT1rAVveE9J6Okg%3D%3D&'
            'searchMtNm=&'
            'searchArNm=&'
            'pageNo=1&'
            'numOfRows=100')

        json_dict = sm.xml_to_json(xml_string)
        body = sm.get_useful_data(json_dict, 1)
        print(body)

    def send_data(self):
        pass


if __name__ == "__main__":
    # sm = ServerMethod()
    main_server = MainServer
    main_server()
