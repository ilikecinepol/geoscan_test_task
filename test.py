import socket
from server_gui import *

ip = '127.0.0.1'
port = 1234
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

server.bind(
    (ip, port)
)
server.listen()

if __name__ == '__main__':

    while True:

        user_socket, address = server.accept()
        user_socket.send("Connected".encode('utf-8'))
        data = user_socket.recv(2048)
        print('fdsf')
        if data:

            print(data.decode('utf-8'))
            if 'name:' in data.decode('utf-8'):
                name = data.decode('utf-8')[5:]
                print(name)
            data = user_socket.recv(2048)
            path = f'server_data/{name}'
            file = open(path, 'wb')
            while data:
                file.write(data)
                data = user_socket.recv(2048)
            file.close()
