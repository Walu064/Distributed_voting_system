import socket
import time
from funcs import generate_number, get_most_common_answer

process_1_decision_list = [9,9,9,9]

if __name__ == '__main__':
    #### Client sockets for process_2, process_3 and process_4:
    ## 1 -> 2
    process_1_to_process_2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## 1 -> 3
    process_1_to_process_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## 1 -> 4
    process_1_to_process_4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    process_1_to_process_2_address = ('localhost', 8000)
    process_1_to_process_3_address = ('localhost', 8001)
    process_1_to_process_4_address = ('localhost', 8002)

    process_1_to_process_2_socket.connect(process_1_to_process_2_address)
    process_1_to_process_3_socket.connect(process_1_to_process_3_address)
    process_1_to_process_4_socket.connect(process_1_to_process_4_address)

    print('Process 1 is running...')

    while True:
        time.sleep(1)
        print("------------- PROCESS_1 -------------")
        message = str(generate_number())
        print("Generated number: "+message)
        process_1_decision_list[0] = message
        
        process_1_to_process_2_socket.sendall(message.encode())
        process_1_to_process_3_socket.sendall(message.encode())
        process_1_to_process_4_socket.sendall(message.encode())

        data_from_process_2 = process_1_to_process_2_socket.recv(1024)
        print('Process_2: ', data_from_process_2.decode())
        process_1_decision_list[1] = data_from_process_2.decode()

        data_from_process_3 = process_1_to_process_3_socket.recv(1024)
        print('Process_3: ', data_from_process_3.decode())
        process_1_decision_list[2] = data_from_process_3.decode()

        data_from_process_4 = process_1_to_process_4_socket.recv(1024)
        print('Process_4: ', data_from_process_4.decode())
        process_1_decision_list[3] = data_from_process_4.decode()

        print('FINAL DECISION Of PROCESS_1: '+get_most_common_answer(process_1_decision_list))