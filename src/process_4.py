import socket
from funcs import generate_number, get_most_common_answer

process_4_decision_list = [9,9,9,9]

if __name__ == '__main__':
    # Server socket - for process_1
    process_1_to_process_4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_1_to_process_4_address = ('localhost', 8002)
    
    process_1_to_process_4_socket.bind(process_1_to_process_4_address)
    process_1_to_process_4_socket.listen(1)

    # Server socket - for process_2
    process_2_to_process_4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_2_to_process_4_address = ('localhost', 8005)
    
    process_2_to_process_4_socket.bind(process_2_to_process_4_address)
    process_2_to_process_4_socket.listen(1)

    # Server socket - for process_3
    process_3_to_process_4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_3_to_process_4_address = ('localhost', 8006)
    
    process_3_to_process_4_socket.bind(process_3_to_process_4_address)
    process_3_to_process_4_socket.listen(1)

    print('Process 4 is running...')

    while True:
        process_1_to_process_4_socket, process_1_to_process_4_address = process_1_to_process_4_socket.accept()
        print('Connection with Process_1', process_1_to_process_4_address)

        process_2_to_process_4_socket, process_2_to_process_4_address = process_2_to_process_4_socket.accept()
        print('Connection with Process_2', process_2_to_process_4_address)    

        process_3_to_process_4_socket, process_3_to_process_4_address = process_3_to_process_4_socket.accept()
        print('Connection with Process_3', process_3_to_process_4_address) 
        
        while True:
            response = str(generate_number())
            print("------------- PROCESS_4 -------------")
            print("Generated number: "+response)
            process_4_decision_list[3] = response

            data_from_process_1 = process_1_to_process_4_socket.recv(1024)
            print('Number from Process_1:', data_from_process_1.decode())
            process_4_decision_list[0] = data_from_process_1.decode()
            try:
                data_from_process_2 = process_2_to_process_4_socket.recv(1024)
                print('Process_2:', data_from_process_2.decode())
                process_4_decision_list[1] = data_from_process_2.decode()

                data_from_process_3 = process_3_to_process_4_socket.recv(1024)
                print('Process_3:', data_from_process_3.decode())
                process_4_decision_list[2] = data_from_process_3.decode()

                process_3_to_process_4_socket.sendall(response.encode())
                process_2_to_process_4_socket.sendall(response.encode())
                process_1_to_process_4_socket.sendall(response.encode())            
            
            except ConnectionError:
                print("Process_3 is not sending data yet.")
            
            except Exception:
                print("Process_3 is not sending data yet.")
            
            print('FINAL DECISION Of PROCESS_4: '+get_most_common_answer(process_4_decision_list))    
        process_1_socket.close()
