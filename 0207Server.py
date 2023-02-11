# 멀티채팅 서버 프로그램
# threading 모듈을 이용한 TCP 멀티채팅서버 프로그램
import json
from socket import *
from threading import *

import pymysql


class ChatserverMulti:
    # 소켓 생성, 연결되면 accept_client() 호출
    def __init__(self):

        self.HOST = '10.10.21.121'
        self.PORT = 3306
        self.USER = 'ElisaBluebell'
        self.PASSWORD = '1234'
        self.DB = 'educationapplication'

        self.clients=[]               # 접속된 클라이언트 소켓 목록
        self.final_received_message='' # 최종 수신 메시지
        self.s_sock=socket(AF_INET,SOCK_STREAM)           # 소켓생성
        # self.ip = '127.0.0.1'
        self.ip = '10.10.21.122'
        # 명은: 122
        self.port= 9030
        self.s_sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) # 주소 재사용
        self.s_sock.bind((self.ip,self.port))             # 연결대기
        print('클라이언트 대기중...')
        self.s_sock.listen(3)                             # 최대 접속인원 3명
        # accept_clinet()를 호출하여 클라이언트와 연결
        self.accept_client()

    # 연결 클라이언트 소켓을 목록에 추가하고 스레드를 생성하여 데이터 수신
    def accept_client(self):
        while True:
            client = c_socket,(ip,port) = self.s_sock.accept() # conn, addr
            if client not in self.clients:      # 만약에 연결클라이언트가 접속된 클라이어트 소켓목록에 없으면
                self.clients.append(client)     # 접속된 소켓을 목록에 추가
            print(f'{ip}:{str(port)}가 연결되었습니다')

            cth = Thread(target = self.receive_message, args=(c_socket,))    # 수신 스레드
            cth.start()                                                     # 스레드 시작

    # 데이터를 수신, 처리 (모든 클라이언트에게 전송)
    def receive_message(self,c_socket):
        '''
        log : 로그인
        acc : 중복체크
        new : 회원가입
        cl0 : 채팅방 생성
        cl1 : 채팅방 조회
        cht : 채팅
        '''
        while True:
            try:
                incoming_message = c_socket.recv(256)
                if not incoming_message: # 연결이 종료됨
                    break
            except:
                continue
            else: # 예외가 발생하지 않아 except절을 실행하지 않았을 경우 실행됨.

                data = incoming_message.decode('utf-8')
                # 이 상태에서 식별자 체크. 문자열의 0,1,2 인덱스 까지가 식별자이다.
                request = data[0:3] # 식별자
                if len(data) > 3:
                    data = data[3:] # 메시지
                    print('<< 클라이언트 요청:', request, '| 데이터:', data)
                    # json.loads()로 문자열을 본래 자료형으로 변환
                    data = json.loads(data)
                    # print(type(data))
                else: data = None # 메시지가 없을 경우


                if request != 'cht': #식별자가 채팅이 아닐 때
                    if request == 'log' :
                        # print('로그인 실행')
                        # 로그인 함수를 실행하여 클라이언트로 전달
                        result = self.login_user(data) # DB 조회 결과, 문자열
                        self.send_request_client(c_socket, result)

                    elif request == 'acc': ######################명은
                        print('회원조회 실행')
                        result = self.check_user(data)
                        self.send_request_client(c_socket, result)
                        print('회원조회 완료')

                    elif request == 'new':
                        print('회원추가 실행')
                        result = self.new_user(data)
                        print('회원추가 완료')

                    elif request == 'cl0':
                        print('채팅방 생성')

                    elif request == 'cl1':
                        print('채팅방 조회')
                        result = self.list_up_room()
                        self.send_request_client(c_socket, result)

                else:
                    print('채팅') # 작성해야됨 !!!!

                # self.final_received_message=incoming_message.decode('utf-8')
                # print(self.final_received_message)
                # self.send_all_client(c_socket) # 메시지 전송
        c_socket.close()


    # 송신 클라이언트를 제외한 모든 클라이언트에게 메시지 전송
    def send_all_client(self,senders_socket):
        for client in self.clients:             # 목록에 있는 모든 소켓에 대해
            socket, (ip,port) = client
            if socket is not senders_socket:    # 송신 클라이언트 제외
                try:
                    socket.sendall(self.final_received_message.encode())
                except: # 연결종료
                    self.clients.remove(client) # 소켓 제거
                    print(f'{ip}:{port} 연결이 종료되었습니다')

    # 요청을 보내온 클라이언트에 응답
    def send_request_client(self, senders_socket, data:str):
        print('>> 송신 클라이언트에 응답 -- ', end='')
        for client in self.clients:             # 목록에 있는 모든 소켓 중 송신 클라이언트에게만 응답
            socket, (ip,port) = client
            if socket is senders_socket:    # 송신 클라이언트
                try:
                    socket.send(data.encode()) # str을 인코딩해 전송
                    # @클라이언트: ~~~~_result 에서 이어서 작성
                except: # 연결종료
                    self.clients.remove(client) # 소켓 제거
                    print(f'{ip}:{port} 연결이 종료되었습니다')


    # DB 접근 -----------------------------------------------------------------------------------------------------------

    # def login_user(self, account:dict):
    #     print('@ 로그인 시도 ID:', account['phone'], '| 타입:', type(account['phone']), end='')
    #     with self.conn_fetch() as cur:
    #         # 휴대폰 번호로 DB 조회
    #         sql = f"SELECT user_name, user_phone, user_pass FROM users WHERE user_phone = '{account['phone']}';"
    #         cur.execute(sql)
    #         result = cur.fetchone()
    #
    #         if result: # 조회 결과가 존재한다면
    #             print(result)  # user_name, user_phone, user_pass
    #             result = json.dumps(result)  # 바이너리화
    #             return 'log' + result
    #         else:
    #             print('None')
    #             return 'log'

    # def check_user(self, account:dict):
    #     print(f"@ 유저 {account['phone']} 조회 --", end='')
    #     with self.conn_fetch() as cur:
    #         sql = f"SELECT user_phone FROM users WHERE user_phone = '{account['phone']}'"
    #         cur.execute(sql, account)
    #         result = cur.fetchone()

        # if result:  # 조회 결과가 존재한다면
        #     print(result)
        #     result = json.dumps(result)  # 바이너리화
        #     #이미 존재하는 유저라고 클라이언트에 전달
        #     return 'acc' + result
        #
        # else: # 조회 결과가 없다면
        #     print('None')
        #     return 'acc'
        #     # return: 조회 결과 없다고 클라이언트에 전달

    def new_user(self, user:tuple): # 회원 추가
        with self.conn_commit() as con:
            with con.cursor() as cur:
                sql = 'INSERT INTO account(class, user_name, user_id, user_password)' \
                      'VALUES ('', '', %s, %s)'
                cur.execute(sql, user)
                con.commit()
        print('회원 추가 완료')

    # def create_room(self, new_room:dict): # 채팅방 생성
    #     # 기존에 같은 제목의 방이 있는지 조회
    #     with self.conn_fetch() as cur:
    #         sql = f"SELECT room_name FROM t8_db.room WHERE room_name = '{new_room['title']}'"  # 채팅방 조회 쿼리
    #         cur.execute(sql)
    #         result = cur.fetchone()
    #         print(result)
    #
    #     if result: # 이미 같은 이름의 채팅방이 존재하는 경우
    #         print('이미 같은 이름의 채팅방이 존재하는 경우')
    #         # 클라이언트에 방이 없다고 전달해야함 !!!!
    #
    #     else: # 같은 이름의 채팅방이 존재하지 않는 경우
    #         with self.conn_commit() as con:
    #             with con.cursor() as cur:
    #                 sql = 'INSERT INTO t8_db.room (room_name, room_master) VALUES (%s, %s)'  # 채팅방 생성 쿼리
    #                 cur.execute(sql, (new_room['title'], new_room['master']))
    #                 con.commit()
    #         print('채팅방 생성')
            # 클라이언트에 완료했다고 전달해야함 !!!!

    # def list_up_room(self): # 채팅방 조회
    #     with self.conn_fetch() as cur:
    #             sql = 'SELECT * FROM t8_db.room;'  # 채팅방 조회 쿼리
    #             cur.execute(sql)
    #             rows = cur.fetchall() # 방 목록
    #     print(rows) #튜플
    #     result = json.dumps(rows)
    #     print(result) #문자열
    #     return 'cl1' + result

    # ------------------------------------------------------------------------------------------------------------------

    # DB 연결용 코드
    def conn_fetch(self):
        con = pymysql.connect(host=self.HOST, user=self.USER, password=self.PASSWORD, db=self.DB, charset='utf8')
        cur = con.cursor()
        return cur

    def conn_commit(self):
        con = pymysql.connect(host=self.HOST, user=self.USER, password=self.PASSWORD, db=self.DB, charset='utf8')
        return con

if __name__=='__main__':
    ChatserverMulti()