import json
import socket
from _thread import *
from nlp_process import classify_pos_neg_sentences, classify_fields, load_jsons


def threaded(client_socket, addr):
    print(">> Connected by ", addr[0], ":", addr[1])

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(">> Disconnected by ", addr[0], ":", addr[1])
                break

            print(">> Received from ", addr[0], ":", addr[1])

            received_data = data.decode('utf-8')
            received_data = json.loads(received_data)
            print(">> Received message: ", received_data)

            if received_data["type"] == "NLP_POS_NEG":
                result = classify_pos_neg_sentences(received_data["data"])
            elif received_data["type"] == "NLP_FIELD":
                result = classify_fields(received_data["data"])

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


client_sockets = []

HOST = '127.0.0.1'
PORT = 9999

print(">> NLP Processor Start")
processor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
processor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
processor_socket.bind((HOST, PORT))
processor_socket.listen()

load_jsons()

try:
    while True:
        print(">> Waiting")

        client_socket, addr = processor_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("Clients: ", len(client_sockets))

except Exception as e:
    print("[Error] ", e)

finally:
    processor_socket.close()
