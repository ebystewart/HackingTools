
import socket


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

listener.bind((("127.0.0.1", 4456)))
listener.listen(0)
print("[+] Waiting for incoming connections")

connection, address = listener.accept()
print("[+] Got a connection from" + str(address))

msg = connection.recv(1024)
print(str(msg))

while True:
    try:
        command = input(">> ")
        connection.send(command.encode())
        result = connection.recv(1024)
        print(result)

    except KeyboardInterrupt:
        print("[+] Detected CTRL + C.....Closing App....Please wait...")
        connection.close()
        exit()
    