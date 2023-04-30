import json
import socket
from _thread import *
from nlp_process import classify_pos_neg_sentences, classify_fields, load_jsons

# 클라이언트에서 요청한 작업에 대해 자연어처리를 수행하는 소켓 통신 서버

# 소켓 통신을 위한 클라이언트 스레드 함수
def threaded(client_socket, addr):
    print(">> Connected by ", addr[0], ":", addr[1])

    while True:
        try: 
            # 클라이언트로부터 데이터 수신
            data = client_socket.recv(1024)
            if not data:
                print(">> Disconnected by ", addr[0], ":", addr[1])
                break

            print(">> Received from ", addr[0], ":", addr[1])

            # 수신된 데이터 디코딩 및 JSON 형태로 파싱
            received_data = data.decode('utf-8')
            received_data = json.loads(received_data)
            print(">> Received message: ", received_data)

            # 분류 작업 수행
            if received_data["type"] == "NLP_POS_NEG":
                result = classify_pos_neg_sentences(received_data["data"])
            elif received_data["type"] == "NLP_FIELD":
                result = classify_fields(received_data["data"])

            # 결과 데이터를 JSON 형태로 변환 후 송신
            result = json.dumps(result, ensure_ascii=False)
            print(result)
            client_socket.send(result.encode('utf-8'))
        except ConnectionResetError as e:
            print(">> Disconnected by ", addr[0], ":", addr[1])
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('Remove Client List: ', len(client_sockets))

    client_socket.close()

# 클라이언트 소켓 리스트
client_sockets = []

# 호스트 주소 및 포트
HOST = '0.0.0.0'
PORT = 48088

print(">> NLP Processor Start")
processor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
processor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
processor_socket.bind((HOST, PORT))
processor_socket.listen()

# NLP 분류 작업을 위한 JSON 파일 로드
load_jsons()

try:
    while True:
        # 클라이언트 접속 대기
        print(">> Waiting")

        # 클라이언트 접속
        client_socket, addr = processor_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("Clients: ", len(client_sockets))

except Exception as e:
    print("[Error] ", e)

finally:
    # 소켓 연결 종료
    processor_socket.close()
