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
        self.method = 1
        self.initUI()
        self.matrix_length = 3

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
        r1 = Radiobutton(buttons_frame, text="Гаусс", variable=self.method, value=0, command=self.set_first_method)
        r1.pack(side=LEFT)
        Radiobutton(buttons_frame, text="Обратная", variable=self.method, value=1, command=self.set_second_method).pack(
            side=LEFT)
        r1.select()
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

    def set_first_method(self):
        self.method = 1

    def set_second_method(self):
        self.method = 2

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

    def print_matrix(self, matrix):
        for i in range(self.matrix_length):
            print(matrix[i])

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

        print("Матрица на входе:")
        self.print_matrix(matrix)
        self.sortMatrix(matrix)

        print("После свапа:")
        self.print_matrix(matrix)

        # зануляем всё что ниже диагонали
        for step in range(self.matrix_length - 1):
            for row in range(step + 1, self.matrix_length):
                if(matrix[step][step] == 0):
                    continue
                coefficient = matrix[row][step] / -matrix[step][step]
                for column in range(self.matrix_length + 1):
                    matrix[row][column] += round(coefficient * matrix[step][column], 10)
            print("Зануление, шаг: ", step)
            self.print_matrix(matrix)
            self.sortMatrix(matrix)

        print("После зануления: ")
        self.print_matrix(matrix)

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
            matrix = []
            if self.method == 1:
                X = X - invertW.dot(FX)
            elif self.method == 2:

                for i in range(self.matrix_length):
                    matrix.append([0] * (self.matrix_length + 1))

                for i in range(self.matrix_length):
                    for j in range(self.matrix_length):
                        matrix[i][j] = A[i][j]
                    matrix[i][self.matrix_length] = FX[i][0]
                gaus = self.calculate_gaus(matrix)

                X = X - gaus

        self.print_result(X)


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

def startLab4():
    window = Tk()
    app = fourthLab(window)
    window.mainloop()