from tkinter import *
from PIL import ImageTk, Image
import time
import socket
from tkinter.ttk import Combobox
from tkinter import filedialog as fd


class Client:
    '''Класс графического интерфейса Сервера'''

    def __init__(self, window):
        title = "Клиент для отправки изображений"
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
            stat = Label(window, text=f"IP:{ip}      PORT:{port}", font=("Arial Bold", 24), fg="#555555", bg="#f3f3f3")
            stat.grid(row=2, column=0, columnspan=2)

        output_data()
        file_name = StringVar()
        file_name.set("Выберите файл")
        self.file_name = file_name
        combo_file = Entry(data, width=36, textvariable=file_name)

        combo_file.grid(column=0, row=3, sticky='w')

        browse = Button(data, text="Выбрать файл", height=1, width=30, command=self.browse_file)
        browse.grid(column=0, row=4)

        btn3 = Button(data, text="Применить", height=1, width=30, command=output_data)
        btn3.grid(column=0, row=5)
        btn4 = Button(data, text="Подключение к серверу", height=1, width=30, command=self.connect_to_server)
        btn4.grid(column=0, row=6)

        transmit_button = Button(data, text="Отправить на сервер", height=1, width=30, command=self.send_picture)
        transmit_button.grid(column=0, row=8)

        self.data = data
        self.path = ''

    def get_port(self):
        port = self.combo1.get()
        return port

    def get_ip(self):
        ip = self.combo.get()
        return ip

    def browse_file(self):
        name = fd.askopenfilename()
        self.file_name.set(name)
        self.past_picture(name)
        self.path = name


    def connection_status(self, status):
        color = 'green' if status else 'red'

        # Овальная форма.
        size = 200
        canvas = Canvas(self.data, height=size, width=size)
        canvas.grid(column=0, row=7, sticky='nw')
        canvas.create_oval(
            10, 10, size, size, outline="#f11",
            fill=color, width=2
        )

        return color

    def connect_to_server(self):
        # Логика клиента
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.ip = self.get_ip()
        self.port = self.get_port()
        print(self.ip, self.port)
        try:
            self.client.connect(
                (self.ip, int(self.port))
            )
            data = self.client.recv(2048)
            print(data.decode('utf-8'))
            status = True if data.decode('utf-8') == 'Connected' else False
            print('staus', status)

        except ValueError:
            status = False
            print('Ошибка')
        self.connection_status(status)

    def past_picture(self, path):
        # create a canvas to show image on
        canvas_for_image = Canvas(window, height=350, width=350, borderwidth=0, highlightthickness=0)
        canvas_for_image.grid(row=1, column=1, padx=25, pady=25)

        # create image from image location resize it to 200X200 and put in on canvas
        image = Image.open(path)

        canvas_for_image.image = ImageTk.PhotoImage(image.resize((350, 350), Image.ANTIALIAS))
        canvas_for_image.create_image(1, 1, image=canvas_for_image.image, anchor='nw')

    def get_image_name(self, path):
        num = 0
        path = path[::-1]
        for i in range(len(path)):
            if path[i] == '/':
                num = i
                break
        name = path[:num]
        name = name[::-1]
        return name

    def send_picture(self):
        name = self.get_image_name(self.path)
        print(name)
        self.client.send(f'name:{name}'.encode('utf-8'))
        time.sleep(1)
        file = open(self.path, 'rb')
        data = file.read(2048)
        while data:
            self.client.send(data)
            data = file.read(2048)
        file.close()
        self.client.close()
        self.connection_status(False)


if __name__ == '__main__':
    window = Tk()
    window.title("Server")
    window.geometry("600x600")
    display = Client(window)
    path = 'server_data/spinner.gif'
    display.past_picture(path)
    display.connection_status(False)
    while True:
        window.update()
        time.sleep(0.1)
