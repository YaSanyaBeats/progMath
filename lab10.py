from tkinter import *
from tkinter import filedialog
from errors import errorCodes, error
import math
import numpy as np
import matplotlib.pyplot as plt

M = 2

# 0 0.1
# 0.5 0.2
# 1 0.6
# 1.5 1.1
# 2 2
# 2.5 3.3


class tenLab():
    def __init__(self, window):
        super().__init__()
        self.window = window  # родительское окно в методе
        self.coefficients = []
        self.inputs = []
        self.initUI()
        self.Y = []
        self.X = []
        self.matrix_length = 3

    def initUI(self):
        self.window.title("Аппроксимация #7")

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
        input6 = Entry(master=main_frame_x, width=10)
        input1.pack(side=LEFT)
        input2.pack(side=LEFT)
        input3.pack(side=LEFT)
        input4.pack(side=LEFT)
        input5.pack(side=LEFT)
        input6.pack(side=LEFT)

        main_frame_x.pack(side=TOP, padx=10)

        main_frame_y = Frame(master=self.window)
        Label(master=main_frame_y, text="y: ").pack(side=LEFT)
        input7 = Entry(master=main_frame_y, width=10)
        input8 = Entry(master=main_frame_y, width=10)
        input9 = Entry(master=main_frame_y, width=10)
        input10 = Entry(master=main_frame_y, width=10)
        input11 = Entry(master=main_frame_y, width=10)
        input12 = Entry(master=main_frame_y, width=10)

        input7.pack(side=LEFT)
        input8.pack(side=LEFT)
        input9.pack(side=LEFT)
        input10.pack(side=LEFT)
        input11.pack(side=LEFT)
        input12.pack(side=LEFT)

        main_frame_y.pack(side=TOP, padx=10)

        self.inputs = [input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12]

        result_frame = Frame(master=self.window)
        result_frame.pack(side=TOP)
        self.result_label = Label(master=result_frame, font="Courier 16", pady=10)
        self.result_label.pack(side=TOP)

    def calculate(self):
        for i in range(6):
            self.X.append(float(self.inputs[i].get()))

        for i in range(6, 12):
            self.Y.append(float(self.inputs[i].get()))

        matrix = self.initMatrix()
        roots = self.gauss(matrix, len(matrix))
        print("\nКорни", roots)

        interval = np.arange(self.X[0], self.X[5], 0.1)
        funcVal = []

        for i in range(len(interval)):
            funcVal.append(self.approxFunc(roots, interval[i]))

        self.graph(interval, funcVal, "~x^2", 1)
        for i in range(len(self.X)):
            plt.scatter(self.X[i], self.Y[i])
        plt.show()

    def sortMatrix(self, matrix, mLen):
        rowMaxElem = 0
        for i in range(mLen):
            for j in range(i + 1, mLen):
                column = 0
                while matrix[i][column] == matrix[j][column]:
                    column += 1
                    if column == mLen + 1:
                        return
                if abs(matrix[i][column]) < abs(matrix[j][column]):
                    matrix[:, [i, j]] = matrix[:, [j, i]]

    def printMatrix(self, matrix, mLen):
        for i in range(mLen):
            print(matrix[i])

    def gauss(self, matrix, mLen):
        print("Исходная матрица:")
        self.printMatrix(matrix, mLen)

        self.sortMatrix(matrix, mLen)

        for step in range(mLen - 1):
            for row in range(step + 1, mLen):
                if (matrix[step][step] == 0):
                    continue
                coefficient = matrix[row][step] / -matrix[step][step]
                for column in range(mLen + 1):
                    matrix[row][column] += round(coefficient * matrix[step][column], 10)
            self.sortMatrix(matrix, mLen)

        step = 0
        results = []
        for row in range(mLen - 1, -1, -1):
            count = 0
            for column in range(mLen - 1, mLen - step - 1, -1):
                matrix[row][mLen] -= matrix[row][column] * results[count]
                count += 1
            results.append(round(matrix[row][mLen] / matrix[row][mLen - step - 1], 3))
            step += 1

        return np.array(results)

    def sumX(self, step):
        sum = 0
        for i in range(len(self.X)):
            sum += self.X[i] ** step
        return sum

    def sumY(self, step):
        sum = 0
        for i in range(len(self.X)):
            sum += self.Y[i] * (self.X[i] ** step)
        return sum

    def initMatrix(self):
        matrix = np.empty((M + 1, M + 2))
        for i in range(M + 1):
            for j in range(M + 1):
                matrix[i][j] = self.sumX(i + j)
            matrix[i][len(matrix[i]) - 1] = self.sumY(i)
        return matrix

    def graph(self, X, Y, descr, figureNum):
        plt.figure(figureNum)
        plt.plot(X, Y, label=descr)
        plt.legend()

    def approxFunc(self, roots, x):
        sum = 0
        for i in range(len(roots)):
            sum += roots[i] * (x ** i)
        return sum

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

def startLab10():
    window = Tk()
    app = tenLab(window)
    window.mainloop()