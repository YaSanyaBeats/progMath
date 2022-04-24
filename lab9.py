from tkinter import *
from tkinter import filedialog
from errors import errorCodes, error
import math
import numpy as np
import matplotlib.pyplot as plt

E = 0.0001

def func1(x):
    return 1 / x

def func2(x):
    return x ** 2

def func3(x):
    return x + 4

class nineLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.start = 1.0
        self.end = 2.0
        self.n = 10
        self.step = abs((self.end - self.start) / self.n)
        self.interval = np.arange(self.start, self.end + self.step, self.step)
        self.current_function = func1
        self.initUI()

    def initUI(self):
        self.window.title("Интегрирование с двойным пересчётом #9")

        buttons_frame = Frame(master=self.window, padx=10, pady=5)
        self.button1 = Button(text="1/x", master=buttons_frame, width=10, command=lambda f=func1: self.open_graph(f))
        self.button1.pack(side=LEFT)
        self.button2 = Button(text="x^2", master=buttons_frame, width=10, command=lambda f=func2: self.open_graph(f))
        self.button2.pack(side=LEFT)
        self.button3 = Button(text="x+4", master=buttons_frame, width=10, command=lambda f=func3: self.open_graph(f))
        self.button3.pack(side=LEFT)
        buttons_frame.pack(side=TOP)

        self.result_label = Label(master=self.window, font="Courier 16", padx=10, pady=5, text="")
        self.result_label.pack(side=TOP)

    def open_graph(self, function):
        self.current_function = function
        result = "Trapezoid: "
        result += str(self.doubleCalcTrap(self.start, self.end, self.step, self.interval))
        result += "\nSimpson: "
        result += str(self.doubleCalcSimp(self.start, self.end, self.step, self.interval))
        self.print_result(result)

    def print_result(self, result):
        self.result_label.config(text=result)

    def trapezoidFormula(self, interval, step):
        sum = 0
        for i in range(1, len(interval) - 1, 1):
            sum += self.current_function(interval[i])
        sum += (self.current_function(interval[0]) + self.current_function(interval[len(interval) - 1])) / 2
        return sum * step


    def simpsonFormula(self, interval, step):
        sum = 0
        for i in range(1, len(interval) - 1, 1):
            if i % 2 == 1:
                sum += 4 * self.current_function(interval[i])
            else:
                sum += 2 * self.current_function(interval[i])
        sum += self.current_function(interval[0]) + self.current_function(interval[len(interval) - 1])
        return sum * (step / 3)


    def doubleCalcTrap(self, start, end, step, interval):
        print("Trapezoid:")
        integrals = []
        for i in range(2):
            integrals.append(self.trapezoidFormula(interval, step))
            step /= 2
            interval = np.arange(start, end + step, step)
            print(integrals[i])

        i = 0
        while abs(integrals[i] - integrals[i + 1]) > E * 3:
            integrals.append(self.trapezoidFormula(interval, step))
            step /= 2
            interval = np.arange(start, end + step, step)
            print(integrals[i + 2])
            i += 1
        print("\n")
        return str(integrals[i + 1])


    def doubleCalcSimp(self, start, end, step, interval):
        print("Simpson:")
        integrals = []
        for i in range(2):
            integrals.append(self.simpsonFormula(interval, step))
            step /= 2
            interval = np.arange(start, end + step, step)
            print(integrals[i])

        i = 0
        while abs(integrals[i] - integrals[i + 1]) > E * 3:
            integrals.append(self.simpsonFormula(interval, step))
            step /= 2
            interval = np.arange(start, end + step, step)
            print(integrals[i + 2])
            i += 1
        print("\n")
        return str(integrals[i + 1])


def startLab9():
    window = Tk()
    app = nineLab(window)
    window.mainloop()