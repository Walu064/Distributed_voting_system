import socket
from funcs import generate_number, get_most_common_answer

process_2_decision_list = [9,9,9,9]
process_3_flag = 0

if __name__ == '__main__':
    # Server socket - for process_1
    process_1_to_process_2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_1_to_process_2_address = ('localhost', 8000)
    
    process_1_to_process_2_socket.bind(process_1_to_process_2_address)
    process_1_to_process_2_socket.listen(1)

    # Client socket - for process_3
    process_2_to_process_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_2_to_process_3_address = ('localhost', 8004)

    # Client socket - for process_4
    process_2_to_process_4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_2_to_process_4_address = ('localhost', 8005)

    print('Process 2 is running...')

    while True:
        process_1_to_process_2_socket, process_1_to_process_2_address = process_1_to_process_2_socket.accept()
        print('Connection with Process_1', process_1_to_process_2_address)
        
        while True:
            response = str(generate_number())
            print("------------- PROCESS_2 -------------")
            print("Generated number: "+response)
            process_2_decision_list[1] = response

            data_from_process_1 = process_1_to_process_2_socket.recv(1024)
            print('Process_1:', data_from_process_1.decode())
            process_2_decision_list[0] = data_from_process_1.decode()
            
            if process_2_decision_list[0] != 9:
                if process_3_flag == 0:
                    process_2_to_process_3_socket.connect(process_2_to_process_3_address)
                    process_2_to_process_4_socket.connect(process_2_to_process_4_address)
                    process_3_flag = 1
                
                process_2_to_process_3_socket.sendall(response.encode())
                process_2_to_process_4_socket.sendall(response.encode())
                process_1_to_process_2_socket.sendall(response.encode())

                data_from_process_3 = process_2_to_process_3_socket.recv(1024)
                print('Process_3: ', data_from_process_3.decode())
                process_2_decision_list[2] = data_from_process_3.decode()

                data_from_process_4 = process_2_to_process_4_socket.recv(1024)
                print("Process_4: "+data_from_process_4.decode())
                process_2_decision_list[3] = data_from_process_4.decode()
                
                print('FINAL DECISION Of PROCESS_1: '+get_most_common_answer(process_2_decision_list))
        
        process_1_socket.close()
        process_2_to_process_3_socket.close()
