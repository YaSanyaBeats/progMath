from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error
import math
import numpy as np
import matplotlib.pyplot as plt

class seventhLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.method = "1"
        self.coefficients = []
        self.inputs = []
        self.initUI()
        self.Y = []
        self.X = []
        self.matrix_length = 3

    def initUI(self):
        self.window.title("Сплайны #7")

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
        input5 = Entry(master=main_frame_x, width=10)
        input1.pack(side=LEFT)
        input2.pack(side=LEFT)
        input3.pack(side=LEFT)
        input4.pack(side=LEFT)
        input5.pack(side=LEFT)

        main_frame_x.pack(side=TOP, padx=10)

        main_frame_y = Frame(master=self.window)
        Label(master=main_frame_y, text="y: ").pack(side=LEFT)
        input6 = Entry(master=main_frame_y, width=10)
        input7 = Entry(master=main_frame_y, width=10)
        input8 = Entry(master=main_frame_y, width=10)
        input9 = Entry(master=main_frame_y, width=10)
        input10 = Entry(master=main_frame_y, width=10)
        input5.pack(side=LEFT)
        input6.pack(side=LEFT)
        input7.pack(side=LEFT)
        input8.pack(side=LEFT)
        input9.pack(side=LEFT)
        input10.pack(side=LEFT)
        main_frame_y.pack(side=TOP, padx=10)

        sub_frame = Frame(master=self.window)
        Label(master=sub_frame, text="Рассчитать от x:").pack(side=LEFT)
        input11 = Entry(master=sub_frame, width=10)
        input11.pack(side=LEFT)
        sub_frame.pack(side=TOP)

        self.inputs = [input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11]

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
            y.append(self.calculate_digit(x[i]))
        plt.plot(x, y)
        plt.show()

    def sortMatrix(self, matrix):
        # сортировка строк по убыванию (пузырёк)
        rowMaxElem = 0
        for i in range(self.matrix_length):
            for j in range(i + 1, self.matrix_length):
                # сравнение строк матрицы
                column = 0
                while matrix[i][column] == matrix[j][column]:
                    column += 1
                    if column == self.matrix_length + 1:
                        error(errorCodes.IDENTIAL_LINES)
                        return
                if abs(matrix[i][column]) < abs(matrix[j][column]):  # по убыванию
                    matrix[i], matrix[j] = matrix[j], matrix[i]

    def calculate_gaus(self, matrix):

        self.sortMatrix(matrix)

        # зануляем всё что ниже диагонали
        for step in range(self.matrix_length - 1):
            for row in range(step + 1, self.matrix_length):
                if(matrix[step][step] == 0):
                    continue
                coefficient = matrix[row][step] / -matrix[step][step]
                for column in range(self.matrix_length + 1):
                    matrix[row][column] += round(coefficient * matrix[step][column], 10)
            self.sortMatrix(matrix)

        # находим неизвестные
        step = 0
        results = []
        for row in range(self.matrix_length - 1, -1, -1):
            count = 0
            for column in range(self.matrix_length - 1, self.matrix_length - step - 1, -1):
                matrix[row][self.matrix_length] -= matrix[row][column] * results[count]
                count += 1
            results.append(matrix[row][self.matrix_length] / matrix[row][self.matrix_length - step - 1])
            step += 1

        results.reverse()

        return np.array([[results[0]], [results[1]], [results[2]]])

    def get_step_x(self, i):
        return self.X[i + 1] - self.X[i]

    def get_step_x2(self, i):
        return self.X[i] - self.X[i - 1]

    def get_step_y(self, i):
        return self.Y[i + 1] - self.Y[i]

    def calculate(self):
        self.coefficients = self.get_coef()
        result = self.calculate_digit(self.coefficients[10])
        self.print_result(str(result))

    def calculate_digit(self, x):
        self.X = np.array(self.coefficients[0:5])
        self.Y = np.array(self.coefficients[5:10])

        C = np.empty((3, 3))
        for i in range(3):
            for j in range(3):
                if i == j:
                    C[i][j] = (self.get_step_x(i) + self.get_step_x(i + 1)) / 3
                elif i == j - 1:
                    C[i][j] = self.get_step_x(i + 1) / 6
                elif i == j + 1:
                    C[i][j] = self.get_step_x(i) / 6
                else:
                    C[i][j] = 0

        D = np.empty((3, 1))
        for i in range(3):
            D[i][0] = self.get_step_y(i + 1) / self.get_step_x(i + 1) - self.get_step_y(i) / self.get_step_x(i)

        CD = np.hstack((C, D))

        M = np.round(np.array(self.calculate_gaus(CD)), 2)
        M = np.vstack((0, M, 0))

        i = 0
        while x > self.X[i]:
            i += 1

        result = 0
        result += M[i - 1][0] * (self.X[i] - x) ** 3 / 6 / self.get_step_x2(i)
        result += M[i][0] * (x - self.X[i - 1]) ** 3 / 6 / self.get_step_x2(i)
        result += (self.Y[i - 1] - M[i - 1][0] * self.get_step_x2(i) ** 2 / 6) * (self.X[i] - x) / self.get_step_x2(i)
        result += (self.Y[i] - M[i][0] * self.get_step_x2(i) ** 2 / 6) * (x - self.X[i - 1]) / self.get_step_x2(i)

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


def startLab7():
    window = Tk()
    app = seventhLab(window)
    window.mainloop()
