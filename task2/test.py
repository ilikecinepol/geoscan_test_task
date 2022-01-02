import socket
import time

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

client.connect(
    ('127.0.0.1', 1234)
)
data = client.recv(2048)
print(data.decode('utf-8'))


def get_image_name(path):
    num = 0
    path = path[::-1]
    for i in range(len(path)):
        if path[i] == '/':
            num = i
            break
    name = path[:num]
    name = name[::-1]
    return name


path = 'client_data/pioner.jpg'


def send_picture(path):
    name = get_image_name(path)
    print(name)
    client.send(f'name:{name}'.encode('utf-8'))
    time.sleep(1)
    file = open(path, 'rb')
    data = file.read(2048)
    while data:
        client.send(data)
        data = file.read(2048)
    file.close()
    client.close()


# client.close()
send_picture(path)
