from tkinter import *
from PIL import ImageTk, Image
import time
from server import *
from tkinter.ttk import Combobox


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

        def get_ip():
            ip = combo.get()
            return ip

        btn = Button(data, text="IP", height=1, width=5, command=get_ip)
        btn.grid(column=0, row=1, sticky='e')
        combo1 = Combobox(data)
        combo1['values'] = (1234, "loading...")
        combo1.current(1)  # вариант по умолчанию
        combo1.grid(column=0, row=2, sticky='w')

        def get_port():
            port = combo1.get()
            return port

        btn1 = Button(data, text="port", height=1, width=5, command=get_port)
        btn1.grid(column=0, row=2, sticky='e')

        self.ip = get_ip()
        self.port = get_port()
        # output_data(self.ip, self.port)

        def output_data():
            ip = combo.get()
            port = combo1.get()
            lbl = Label(window, text=title, font=("Arial Bold", 24), fg="#ff3300", bg="#f3f3f3")
            lbl.grid(row=0, column=0, columnspan=2)
            stat = Label(window, text=f"IP:{ip} PORT:{port}", font=("Arial Bold", 24), fg="#555555", bg="#f3f3f3")
            stat.grid(row=2, column=0, columnspan=2)
        output_data()

        btn3 = Button(data, text="Start server", height=1, width=30, command=output_data)
        btn3.grid(column=0, row=3)

    def past_picture(self, path):
        # create a canvas to show image on
        canvas_for_image = Canvas(window, height=400, width=400, borderwidth=0, highlightthickness=0)
        canvas_for_image.grid(row=1, column=1, padx=0, pady=0)

        # create image from image location resize it to 200X200 and put in on canvas
        image = Image.open(path)

        canvas_for_image.image = ImageTk.PhotoImage(image.resize((400, 400), Image.ANTIALIAS))
        canvas_for_image.create_image(1, 1, image=canvas_for_image.image, anchor='nw')


if __name__ == '__main__':
    window = Tk()
    window.title("Server")
    window.geometry("600x600")
    display = GUI(window)
    path = 'server_data/load.png'
    display.past_picture(path)

    window.configure(background='#f3f3f3')

    window.mainloop()
