from tkinter import *
from tkinter import filedialog
from errors import errorCodes, error
import math
import numpy as np
import matplotlib.pyplot as plt

E = 0.00001

def dydx1(x, y):
    return math.sin(x) # исходная функция -cos(x)

def dydx2(x, y):
    return 4 * x  # исходная функция 2x^2 - 1

def dydx3(x, y):
    return x * y # исходная функция y

class twelveLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.current_function = dydx1
        self.x0 = 0
        self.y0 = -1
        self.x = 1
        self.h = 0.1

        self.initUI()

    def initUI(self):
        self.window.title("Решение ДУ с двойным пересчётом #12")

        buttons_frame = Frame(master=self.window, padx=10, pady=5)
        self.button1 = Button(text="sin(x)", master=buttons_frame, width=10, command=lambda f=dydx1: self.calculate(f))
        self.button1.pack(side=LEFT)
        self.button2 = Button(text="4x", master=buttons_frame, width=10, command=lambda f=dydx2: self.calculate(f))
        self.button2.pack(side=LEFT)
        self.button3 = Button(text="xy", master=buttons_frame, width=10, command=lambda f=dydx3: self.calculate(f))
        self.button3.pack(side=LEFT)
        buttons_frame.pack(side=TOP)

        self.result_label = Label(master=self.window, font="Courier 16", padx=10, pady=5, text="")
        self.result_label.pack(side=TOP)

    def print_result(self, result):
        self.result_label.config(text="Y(1) = " + str(result))

    def calculate(self, function):
        self.current_function = function
        funcVal = self.rungeKutta4x(self.x0, self.y0, self.x, self.h)

        for i in range(len(funcVal)):
            print('Y({0}) = {1}'.format(self.x, funcVal[i]))

        self.print_result(funcVal[len(funcVal) - 1])

    def rungeKutta4x(self, x0, y0, x, h):
        funcVal = []
        x0Copy = x0

        for i in range(2):
            x0 = x0Copy
            n = (int)((x - x0) / h)
            y = y0
            for j in range(n):
                k1 = h * self.current_function(x0, y)
                k2 = h * self.current_function(x0 + 0.5 * h, y + 0.5 * k1)
                k3 = h * self.current_function(x0 + 0.5 * h, y + 0.5 * k2)
                k4 = h * self.current_function(x0 + h, y + k3)

                y += (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

                x0 += h
            funcVal.append(y)
            h /= 2

        x0 = x0Copy
        n = (int)((x - x0) / h)
        y = y0

        i = 0
        while abs(funcVal[i] - funcVal[i + 1]) > E * 15:
            for j in range(1, n + 1):
                k1 = h * self.current_function(x0, y)
                k2 = h * self.current_function(x0 + 0.5 * h, y + 0.5 * k1)
                k3 = h * self.current_function(x0 + 0.5 * h, y + 0.5 * k2)
                k4 = h * self.current_function(x0 + h, y + k3)

                y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

                x0 = x0 + h
            funcVal.append(y)
            h /= 2
        return funcVal

def startLab12():
    window = Tk()
    app = twelveLab(window)
    window.mainloop()