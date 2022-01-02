import socket



class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        serv = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        serv.bind(
            (ip, port)
        )
        serv.listen()
        self.serv = serv

    def recieve_picture(self):
        user_socket, address = self.serv.accept()
        user_socket.send("Connected".encode('utf-8'))
        print('Server starting')
        user_socket = user_socket
        data = user_socket.recv(2048)
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
        return path


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 1234
    server = Server(ip, port)
    while True:
        server.recieve_picture()
