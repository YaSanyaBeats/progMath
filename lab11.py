from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error
import math
import numpy as np
import matplotlib.pyplot as plt

# 5x^4 + 8x^3 + 2x^2 + x + 1

class elevenLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.coefficients = []
        self.inputs = []
        self.method = 1
        self.initUI()
        self.matrix_length = 3

    def initUI(self):
        self.window.title("Поиск минимума с помощью золотого сечения #11")

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

        matrix_frame = Frame(master=self.window, pady=10, padx=10)
        for i in range(1):
            current_frame = Frame(master=matrix_frame)
            for j in range(5):
                input = Entry(master=current_frame, width=5)
                self.inputs.append(input)
                input.pack(side=LEFT)
                Label(master=current_frame, text="x^").pack(side=LEFT)
                input = Entry(master=current_frame, width=5)
                self.inputs.append(input)
                input.pack(side=LEFT)
                Label(master=current_frame, text="+").pack(side=LEFT)
            Label(master=current_frame, text=" = 0").pack(side=LEFT)
            current_frame.pack(side=TOP)

        start_frame = Frame(master=matrix_frame)

        Label(master=start_frame, text="A = ").pack(side=LEFT)
        input1 = Entry(master=start_frame, width=5)
        self.inputs.append(input1)
        input1.pack(side=LEFT, padx=10, pady=10)

        Label(master=start_frame, text="B = ").pack(side=LEFT)
        input2 = Entry(master=start_frame, width=5)
        self.inputs.append(input2)
        input2.pack(side=LEFT, padx=10, pady=10)

        start_frame.pack(side=TOP)

        exp_frame = Frame(master=matrix_frame, pady=10)
        Label(master=exp_frame, padx=10, text="Погрешность: ").pack(side=LEFT)
        input = Entry(master=exp_frame, width=5)
        self.inputs.append(input)
        input.pack(side=LEFT, padx=10, pady=10)
        exp_frame.pack(side=TOP)

        matrix_frame.pack(side=TOP)

        result_frame = Frame(master=self.window)
        result_frame.pack(side=TOP)
        self.result_label = Label(master=result_frame, font="Courier 16", pady=10)
        self.result_label.pack(side=TOP)

    def calculate(self):

        f = []
        for i in range(0, 8, 2):
            f.append({'coef': float(self.inputs[i].get()), 'degree': float(self.inputs[i + 1].get())})

        a = float(self.inputs[10].get())
        b = float(self.inputs[11].get())

        f_der = self.get_derivative(f)
        x = np.arange(a, b, 0.1)
        y = []
        for i in range(len(x)):
            y.append(self.calc_function(x[i], f))
        y = np.array(y)
        plt.plot(x, y)
        result = self.search_min(a, b, f_der)
        self.print_result(str(result))
        plt.scatter(result, self.calc_function(result, f))
        plt.show()


    def print_result(self, result):
        self.result_label.config(text="min = " + result)

    def get_derivative(self, function):
        result = []
        for i in range(len(function)):
            current_coef = function[i]['coef'] * function[i]['degree']
            current_degree = function[i]['degree'] - 1
            if current_degree >= 0:
                result.append({'coef': current_coef, 'degree': current_degree})

        return result

    def calc_function(self, x, function_der):
        result = 0
        for i in range(len(function_der)):
            result += function_der[i]['coef'] * (x ** function_der[i]['degree'])
        return result

    def search_min(self, a, b, f_der):
        if abs(b - a) < float(self.inputs[12].get()):
            return (a + b) / 2

        ratio = 0.382
        result = 0

        left_separator = a + ratio * (b - a)
        right_separator = b - ratio * (b - a)

        left_y = self.calc_function(left_separator, f_der)
        right_y = self.calc_function(right_separator, f_der)

        if left_y > 0 and right_y > 0:
            result = self.search_min(a, left_separator, f_der)

        if left_y < 0 < right_y:
            result = self.search_min(left_separator, right_separator, f_der)

        if left_y < 0 and right_y < 0:
            result = self.search_min(right_separator, b, f_der)
        return result

    def clear(self):
        for input in self.inputs:
            input.delete(0, END)
        self.result_label.config(text="")

    def on_open(self):
        self.clear()

        ftypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*')]
        fold = filedialog.askopenfilename(filetypes=ftypes)
        try:
            text = self.read_file(fold)
        except FileNotFoundError:
            error(errorCodes.FILE_NOT_FOUND)
            return

        # разделяем весь текст через пробел в массив
        matrix_elems = text.split(" ")

        # заполняем инпуты
        for index, input in enumerate(self.inputs):
            input.delete(0, END)
            input.insert(0, matrix_elems[index])

    def read_file(self, filename):
        with open(filename, "r") as f:
            text = f.read()
        return text



def startLab11():
    window = Tk()
    app = elevenLab(window)
    window.mainloop()