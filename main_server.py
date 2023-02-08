import server_tool as st
import education_application_utility as eau


class MainServer:
    def __init__(self):
        xml_string = st.get_database_from_url('http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?serviceKey=yn8uwUR3eheqowtPnA9QRTQ9i8mYGhGEetp6HDG1hMhCeH9%2BNJFN6WlIM1AzfgrZB59syoKUT1rAVveE9J6Okg%3D%3D&searchMtNm=&searchArNm=&pageNo=1&numOfRows=100')
        raw_data = st.xml_to_json(xml_string)
        mntnm, aeatreason, overview, details = eau.get_useful_data(raw_data)
        server_socket, socks = st.socket_initialize('10.10.21.121', 9000)
        st.turn_server_on(eau.command_processor, server_socket, socks)


if __name__ == "__main__":
    main_server = MainServer
    main_server()
