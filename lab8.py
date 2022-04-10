from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error
import math
import numpy as np
import matplotlib.pyplot as plt

class eightLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.method = "1"
        self.coefficients = []
        self.inputs = []
        self.initUI()
        self.Y = []
        self.X = []

    def initUI(self):
        self.window.title("Тригонометрическая интерполяция #8")

        mainMenu = Menu(self.window, tearoff=0)  # создаём вкладку в меню
        self.window.config(menu=mainMenu)
        fileMenu = Menu(mainMenu, tearoff=0)  # вкладываем туда кнопки
        fileMenu.add_command(label="Открыть", command=self.on_open)
        mainMenu.add_cascade(label="Файл", menu=fileMenu)

        buttons_frame = Frame(master=self.window, padx=10, pady=5)
        self.clear_button = Button(text="Очистить", master=buttons_frame, width=10, command=self.clear)
        self.clear_button.pack(side=LEFT)
        self.start_button = Button(text="Рассчитать", master=buttons_frame, width=10, command=self.calculate)
        self.start_button.pack(side=LEFT)
        buttons_frame.pack(side=TOP)

        main_frame_x = Frame(master=self.window)
        Label(master=main_frame_x, text="x: ").pack(side=LEFT)
        input1 = Entry(master=main_frame_x, width=10)
        input2 = Entry(master=main_frame_x, width=10)
        input3 = Entry(master=main_frame_x, width=10)
        input4 = Entry(master=main_frame_x, width=10)
        input1.pack(side=LEFT)
        input2.pack(side=LEFT)
        input3.pack(side=LEFT)
        input4.pack(side=LEFT)

        main_frame_x.pack(side=TOP, padx=10)

        main_frame_y = Frame(master=self.window)
        Label(master=main_frame_y, text="y: ").pack(side=LEFT)
        input5 = Entry(master=main_frame_y, width=10)
        input6 = Entry(master=main_frame_y, width=10)
        input7 = Entry(master=main_frame_y, width=10)
        input8 = Entry(master=main_frame_y, width=10)
        input5.pack(side=LEFT)
        input6.pack(side=LEFT)
        input7.pack(side=LEFT)
        input8.pack(side=LEFT)
        main_frame_y.pack(side=TOP, padx=10)

        sub_frame = Frame(master=self.window)
        Label(master=sub_frame, text="Рассчитать от x:").pack(side=LEFT)
        input9 = Entry(master=sub_frame, width=10)
        input9.pack(side=LEFT)
        sub_frame.pack(side=TOP)

        self.inputs = [input1, input2, input3, input4, input5, input6, input7, input8, input9]

        result_frame = Frame(master=self.window)
        result_frame.pack(side=TOP)
        self.result_label = Label(master=result_frame, font="Courier 16", pady=10)
        self.result_label.pack(side=TOP)

    def get_coef(self):
        coefs = []
        for input in self.inputs:
            coefs.append(float(input.get()))
        return coefs

    def print_result(self, result):
        self.result_label.config(text="y = " + result)

        window = plt.subplots()
        x = np.arange(self.X[0], self.X[-1], 0.1)
        y = []
        for i in range(len(x)):
            y.append(self.calculate_y(x[i]))
        plt.plot(x, y)
        plt.show()

    def calculate(self):
        self.coefficients = self.get_coef()
        result = self.calculate_y(self.coefficients[8])
        self.print_result(str(result))

    def get_exp_for_a(self, k):
        a = round(math.cos(2 * k * math.pi), 7)
        b = -round(math.sin(2 * k * math.pi), 7)
        return complex(a, b)

    def get_exp_for_y(self, k, j):
        a = round(math.cos(2 * k * j * math.pi), 7)
        b = round(math.sin(2 * k * j * math.pi), 7)
        return complex(a, b)

    def get_a(self, j):
        result = 0
        for i in range(self.n):
            result += self.Y[i] * self.get_exp_for_a(i * j / self.n)
        return result

    def calculate_y(self, x):
        self.X = self.coefficients[0:4]
        self.Y = self.coefficients[4:8]

        self.h = self.X[1] - self.X[0]
        self.n = 4

        result = 0
        for i in range(int(-self.n / 2) + 1, int(self.n / 2) + 1):
            a = self.get_a(i)
            result += a * self.get_exp_for_y((x - self.X[0]) / self.n / self.h, i)

        result *= 1 / self.n

        return result

    def clear(self):
        for input in self.inputs:
            input.delete(0, END)
        self.result_label.config(text="")

    def on_open(self):
        ftypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*')]
        fold = filedialog.askopenfilename(filetypes=ftypes)
        try:
            text = self.read_file(fold)
        except FileNotFoundError:
            error(errorCodes.FILE_NOT_FOUND)
            return

        self.coefficients = text.split(" ")
        for index, input in enumerate(self.inputs):
            input.delete(0, END)
            input.insert(0, self.coefficients[index])

    def read_file(self, filename):
        with open(filename, "r") as f:
            text = f.read()
        return text


def startLab8():
    window = Tk()
    app = eightLab(window)
    window.mainloop()
