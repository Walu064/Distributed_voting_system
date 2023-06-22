import socket
from funcs import generate_number, get_most_common_answer

process_3_decision_list = [9,9,9,9]
process_4_flag = 0

if __name__ == '__main__':
    # Server socket - for process_1
    process_1_to_process_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_1_to_process_3_address = ('localhost', 8001)
    
    process_1_to_process_3_socket.bind(process_1_to_process_3_address)
    process_1_to_process_3_socket.listen(1)

    # Server socket - for process_2
    process_2_to_process_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_2_to_process_3_address = ('localhost', 8004)
    
    process_2_to_process_3_socket.bind(process_2_to_process_3_address)
    process_2_to_process_3_socket.listen(1)

    # Client socket - for process_4
    process_3_to_process_4_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_3_to_process_4_address = ('localhost', 8006)

    print('Process 3 is running...')

    while True:
        process_1_to_process_3_socket, process_1_to_process_3_address = process_1_to_process_3_socket.accept()
        print('Connection with Process_1', process_1_to_process_3_address)
        
        process_2_to_process_3_socket, process_2_to_process_3_address = process_2_to_process_3_socket.accept()
        print('Connection with Process_2', process_2_to_process_3_address)    

        while True:
            response = str(generate_number())
            print("------------- PROCESS_3 -------------")
            print("Generated number: "+response)
            process_3_decision_list[2] = response
            
            data_from_process_1 = process_1_to_process_3_socket.recv(1024)
            print('Process_1:', data_from_process_1.decode())
            process_3_decision_list[0] = data_from_process_1.decode()

            try:
                data_from_process_2 = process_2_to_process_3_socket.recv(1024)
                print('Process_2:', data_from_process_2.decode())
                process_3_decision_list[1] = data_from_process_2.decode()

                process_2_to_process_3_socket.sendall(response.encode())
                process_1_to_process_3_socket.sendall(response.encode())            
            except ConnectionError:
                print("Process_2 is not sending data yet.")
            except Exception:
                print("Process_2 is not sending data yet.")

            if process_3_decision_list[1] != 9:
                if process_4_flag == 0:
                    process_3_to_process_4_socket.connect(process_3_to_process_4_address)
                    process_4_flag = 1
                process_3_to_process_4_socket.sendall(response.encode())
                
                data_from_process_4 = process_3_to_process_4_socket.recv(1024)
                print("Process_4: "+data_from_process_4.decode())
                process_3_decision_list[3] = data_from_process_4.decode()

            print('FINAL DECISION Of PROCESS_3: '+get_most_common_answer(process_3_decision_list))    
               

        process_1_socket.close()
