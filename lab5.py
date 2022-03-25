from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error


class fifthLab():
    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.method = "Лагранж"
        self.coefficients = []
        self.inputs = []
        self.initUI()

    def initUI(self):
        self.window.title("Лагранж и Эйткен #5")

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

        r1 = Radiobutton(buttons_frame, text="Лагранж", variable=self.method, value=0, command=self.set_first_method)
        r1.pack(side=LEFT)
        Radiobutton(buttons_frame, text="Эйткен", variable=self.method, value=1, command=self.set_second_method).pack(side=LEFT)
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

    def get_q(self, step):
        x = self.coefficients[8]
        q = 1
        for i in range(4):
            if i == step:
                continue
            q *= (x - self.coefficients[i])
            q /= (self.coefficients[step] - self.coefficients[i])
        return q

    def print_result(self, result):
        self.result_label.config(text="x = "+str(round(result, 7)))

    def get_p(self, start, end):
        if start == end:
            print("start - ", start, " end - ", end, "result - ", self.coefficients[start + 4])
            return self.coefficients[start + 4]
        x = self.coefficients[8]
        a = self.get_p(start, end - 1) * (x - self.coefficients[end])
        b = self.get_p(start + 1, end) * (x - self.coefficients[start])
        result = (a - b) / (self.coefficients[start] - self.coefficients[end])
        print("start - ", start, " end - ", end, " a - ", a, " b - ", b, " result - ", result)
        return result

    def calculate_eitken(self):
        self.print_result(self.get_p(0, 3))


    def calculate_lagrange(self):
        result = 0
        for i in range(4):
            result += self.coefficients[i + 4] * self.get_q(i)
        return result

    def calculate(self):
        self.coefficients = self.get_coef()
        if self.method == "Лагранж":
            self.print_result(self.calculate_lagrange())
        if self.method == "Эйткен":
            self.print_result(self.calculate_eitken())

    def clear(self):
        for input in self.inputs:
            input.delete(0, END)
        self.result_label.config(text="")

    def set_first_method(self):
        self.method = "Лагранж"

    def set_second_method(self):
        self.method = "Эйткен"

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


def startLab5():
    window = Tk()
    app = fifthLab(window)
    window.mainloop()