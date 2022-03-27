from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error
import math

class sixthLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.method = "1"
        self.coefficients = []
        self.inputs = []
        self.initUI()
        self.y = []
        self.x = []

    def initUI(self):
        self.window.title("Ньютоны #6")

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

        r1 = Radiobutton(buttons_frame, text="Ньютон 1", variable=self.method, value=0, command=self.set_first_method)
        r1.pack(side=LEFT)
        Radiobutton(buttons_frame, text="Ньютон 2", variable=self.method, value=1, command=self.set_second_method).pack(side=LEFT)
        r1.select()
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

        main_frame_x.pack(side=TOP)

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
        main_frame_y.pack(side=TOP)

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
        self.result_label.config(text="x = "+str(round(result, 7)))

    def get_subs(self):
        sub_matrix = []
        for i in range(4):
            sub_matrix.append([0] * 4)
            sub_matrix[0][i] = self.y[i]

        for i in range(1, 4):
            for j in range(0, 4 - i):
                sub_matrix[i][j] = sub_matrix[i - 1][j + 1] - sub_matrix[i - 1][j]

        return sub_matrix

    def get_q1(self, step):
        q = (self.coefficients[8] - self.x[0]) / (self.x[1] - self.x[0])
        result = 1
        for i in range(step):
            result *= q - i
        return result

    def calculate_1(self):
        result = 0
        for i in range(4):
            result += self.subs[i][0] * self.get_q1(i) / math.factorial(i)
        return result

    def get_q2(self, step):
        q = (self.coefficients[8] - self.x[3]) / (self.x[1] - self.x[0])
        result = 1
        for i in range(3 - step):
            result *= q + i
        return result

    def calculate_2(self):
        result = 0
        for i in range(3, -1, -1):
            result += self.subs[3 - i][i] * self.get_q2(i) / math.factorial(3 - i)
        return result

    def calculate(self):
        self.coefficients = self.get_coef()
        self.x = self.coefficients[0:4]
        self.y = self.coefficients[4:8]
        self.subs = self.get_subs()
        if self.method == "1":
            self.print_result(self.calculate_1())
        if self.method == "2":
            self.print_result(self.calculate_2())

    def clear(self):
        for input in self.inputs:
            input.delete(0, END)
        self.result_label.config(text="")

    def set_first_method(self):
        self.method = "1"

    def set_second_method(self):
        self.method = "2"

    def on_open(self):
        ftypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*')]
        fold = filedialog.askopenfilename(filetypes=ftypes)
        try:
            text = self.read_file(fold)
        except FileNotFoundError:
            error(errorCodes.FILE_NOT_FOUND)
            return

        self.coefficients = text.split(" ")

    def read_file(self, filename):
        with open(filename, "r") as f:
            text = f.read()
        return text


def startLab6():
    window = Tk()
    app = sixthLab(window)
    window.mainloop()