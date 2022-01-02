from tkinter import *
from PIL import ImageTk, Image
import time
from server import *
from tkinter.ttk import Combobox
from server import *


class GUI:
    '''Класс графического интерфейса Сервера'''

    def __init__(self, window):
        title = "Сервер для вывода изображений"
        # Разбиение окна на сетку 3х3
        window.configure(background='#f3f3f3')
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=2)
        window.rowconfigure(0, weight=1)
        window.rowconfigure(1, weight=2)
        window.rowconfigure(2, weight=1)

        # Наполнение содержанием

        data = Frame(window)
        data.grid(row=1, column=0, sticky='N')
        data.rowconfigure(0, weight=1)
        data.rowconfigure(1, weight=1)
        data.rowconfigure(2, weight=1)

        connect = Label(data, text='Подключение', font=("Arial Bold", 24), fg="#555555", bg="#f3f3f3")
        connect.grid(row=0, column=0)
        combo = Combobox(data)
        combo['values'] = ('127.0.0.1', "loading...")
        combo.current(1)  # вариант по умолчанию
        combo.grid(column=0, row=1, sticky='w')

        btn = Button(data, text="IP", height=1, width=5, command=self.get_ip)
        btn.grid(column=0, row=1, sticky='e')
        combo1 = Combobox(data)
        combo1['values'] = (1234, "loading...")
        combo1.current(1)  # вариант по умолчанию
        combo1.grid(column=0, row=2, sticky='w')
        self.combo1 = combo1
        self.combo = combo

        btn1 = Button(data, text="port", height=1, width=5, command=self.get_port)
        btn1.grid(column=0, row=2, sticky='e')

        self.ip = self.get_ip()
        self.port = self.get_port()

        # output_data(self.ip, self.port)

        def output_data():
            ip = combo.get()
            port = combo1.get()
            lbl = Label(window, text=title, font=("Arial Bold", 24), fg="#ff3300", bg="#f3f3f3")
            lbl.grid(row=0, column=0, columnspan=2)
            stat = Label(window, text=f"IP:{ip} PORT:{port}", font=("Arial Bold", 24), fg="#555555", bg="#f3f3f3")
            stat.grid(row=2, column=0, columnspan=2)

        output_data()

        btn3 = Button(data, text="Применить", height=1, width=30, command=output_data)
        btn3.grid(column=0, row=3)
        btn4 = Button(data, text="Запуск сервера", height=1, width=30, command=self.starting_server)
        btn4.grid(column=0, row=4)

        self.data = data

    def get_port(self):
        port = self.combo1.get()
        return port

    def get_ip(self):
        ip = self.combo.get()
        return ip

    def connection_status(self, status):
        color = 'green' if status else 'red'

        # Овальная форма.
        size = 200
        canvas = Canvas(self.data, height=size, width=size)
        canvas.grid(column=0, row=5, sticky='nw')
        canvas.create_oval(
            10, 10, size, size, outline="#f11",
            fill=color, width=2
        )

        return color

    def starting_server(self):
        # Логика сервера
        serv = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.connection_status(False)
        self.serv = serv
        self.ip = self.get_ip()
        self.port = self.get_port()
        # print(self.ip, self.port)
        try:
            self.serv.bind(
                (self.ip, int(self.port))
            )
            status = True
            serv.listen()
            self.serv = serv
        except ValueError:
            # print(ValueError)
            status = False

        # print('in funk', status)
        return status


    def past_picture(self, path):
        # create a canvas to show image on
        canvas_for_image = Canvas(window, height=400, width=400, borderwidth=0, highlightthickness=0)
        canvas_for_image.grid(row=1, column=1, padx=0, pady=0)

        # create image from image location resize it to 200X200 and put in on canvas
        image = Image.open(path)

        canvas_for_image.image = ImageTk.PhotoImage(image.resize((400, 400), Image.ANTIALIAS))
        canvas_for_image.create_image(1, 1, image=canvas_for_image.image, anchor='nw')

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


if __name__ == '__main__':
    window = Tk()
    window.title("Server")
    window.geometry("600x600")
    display = GUI(window)
    path = 'server_data/load.png'
    display.past_picture(path)

    window.configure(background='#f3f3f3')
    while True:
        # print('out funk', display.starting_server())
        if display.starting_server():
            print('starting recieve')
            display.recieve_picture()
        window.update()
        time.sleep(0.1)
