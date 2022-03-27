from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error
import numpy as np


class fourthLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.method = "Лагранж"
        self.coefficients = []
        self.inputs = []
        self.initUI()

    def initUI(self):
        self.window.title("СЛУ методом Ньютона")

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
        str = "xyz"
        for i in range(3):
            current_frame = Frame(master=matrix_frame)
            for j in range(3):
                input = Entry(master=current_frame, width=5)
                self.inputs.append(input)
                input.pack(side=LEFT)
                Label(master=current_frame, text=(str[j] + "^")).pack(side=LEFT)
                input = Entry(master=current_frame, width=5)
                self.inputs.append(input)
                input.pack(side=LEFT)
                Label(master=current_frame, text="+").pack(side=LEFT)
            input = Entry(master=current_frame, width=5)
            self.inputs.append(input)
            input.pack(side=LEFT)
            Label(master=current_frame, text=" = 0").pack(side=LEFT)
            current_frame.pack(side=TOP)

        start_frame = Frame(master=matrix_frame)
        Label(master=start_frame, text="X0 = ").pack(side=LEFT)
        for i in range(3):
            input = Entry(master=start_frame, width=5)
            self.inputs.append(input)
            input.pack(side=LEFT, padx=10, pady=10)
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

    def get_coef(self):
        coefs = []
        for input in self.inputs:
            coefs.append(float(input.get()))
        return coefs

    def print_result(self, result):
        result_str = ""
        result_str += "x = " + str(round(result[0][0], 7)) + "\n"
        result_str += "y = " + str(round(result[1][0], 7)) + "\n"
        result_str += "z = " + str(round(result[2][0], 7)) + "\n"

        self.result_label.config(text=result_str)

    def inputXinOriginal(self, start):
        result = []
        for i in range(3):
            y = 0
            curr_equation = self.coefficients[i * 7:(i + 1) * 7]
            for j in range(3):
                y += curr_equation[j * 2] * (start[j][0] ** curr_equation[j * 2 + 1])
            y += curr_equation[6]
            result.append(y)
        return result

    def inputXinDerivative(self, start):
        result = []
        for i in range(3):
            for j in range(3):
                result.append(self.W[i][j]['coef'] * (start[j][0] ** self.W[i][j]['degree']))
        return result

    def calculate(self):
        self.coefficients = self.get_coef()
        inaccuracy = self.coefficients[24]
        X = np.array([[self.coefficients[21]], [self.coefficients[22]], [self.coefficients[23]]])
        self.W = []
        for i in range(3):
            self.W.append([0] * 3)

        lastX = 1
        while inaccuracy < abs(X[0][0] - lastX):
            lastX = X[0]
            for index_row, row in enumerate(self.W):
                for index in range(len(row)):
                    curr_equation = self.coefficients[index_row * 7:(index_row + 1) * 7]
                    self.W[index_row][index] = {"coef": (curr_equation[index * 2] * curr_equation[(index * 2) + 1]), "degree": (curr_equation[(index * 2) + 1] - 1)}

            currW = self.inputXinDerivative(X)
            currF = self.inputXinOriginal(X)

            A = np.array([currW[0:3], currW[3:6], currW[6:9]])

            invertW = np.linalg.inv(A)
            FX = np.array([[currF[0]], [currF[1]], [currF[2]]])

            X = X - invertW.dot(FX)
        self.print_result(X)


    def clear(self):
        for input in self.inputs:
            input.insert(0, 1)
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

def startLab4():
    window = Tk()
    app = fourthLab(window)
    window.mainloop()