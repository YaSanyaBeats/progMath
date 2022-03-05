from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error

class thirdLab():

    def __init__(self, window):
        super().__init__()
        self.window = window    # родительское окно в методе
        self.initUI()

    def initUI(self):
        self.window.title("Ньютон, половинное деление и хорды #3")

        mainMenu = Menu(self.window, tearoff=0)  # создаём вкладку в меню
        self.window.config(menu=mainMenu)
        fileMenu = Menu(mainMenu, tearoff=0)  # вкладываем туда кнопки
        fileMenu.add_command(label="Открыть", command=self.onOpen)
        mainMenu.add_cascade(label="Файл", menu=fileMenu)

        buttonsFrame = Frame(master=self.window, padx=10, pady=5)
        self.clearButton = Button(text="Очистить", master=buttonsFrame, width=10, command=self.clear)
        self.clearButton.pack(side=LEFT)
        self.startButton = Button(text="Рассчитать", master=buttonsFrame, width=10, command=self.calculate)
        self.startButton.pack(side=LEFT)

        self.method = "Половинное деление"
        r1 = Radiobutton(buttonsFrame, text="Половинное деление", variable=self.method, value=0, command=self.setFirstMethod)
        Radiobutton(buttonsFrame, text="Хорды", variable=self.method, value=1, command=self.setSecondMethod).pack(side=LEFT)
        Radiobutton(buttonsFrame, text="Ньютон", variable=self.method, value=2, command=self.setThirdMethod).pack(side=LEFT)
        r1.select()
        r1.pack(side=LEFT)
        buttonsFrame.pack(side=TOP)

        mainFrame = Frame(master=self.window, padx=10, pady=20)
        input1 = Entry(master=mainFrame, width=10)
        input1.pack(side=LEFT)
        Label(master=mainFrame, text="x² + ").pack(side=LEFT)
        input2 = Entry(master=mainFrame, width=10)
        input2.pack(side=LEFT)
        Label(master=mainFrame, text="x + ").pack(side=LEFT)
        input3 = Entry(master=mainFrame, width=10)
        input3.pack(side=LEFT)
        Label(master=mainFrame, text=" = 0").pack(side=LEFT)
        mainFrame.pack(side=TOP)

        intervalFrame = Frame(master=self.window, padx=10, pady=20)
        Label(master=intervalFrame, text="[").pack(side=LEFT)
        intervalInput1 = Entry(master=intervalFrame, width=5)
        intervalInput1.pack(side=LEFT)
        Label(master=intervalFrame, text=" ; ").pack(side=LEFT)
        intervalInput2 = Entry(master=intervalFrame, width=5)
        intervalInput2.pack(side=LEFT)
        Label(master=intervalFrame, text="] Погрешность: ").pack(side=LEFT)
        accuracyInput = Entry(master=intervalFrame, width=5)
        accuracyInput.pack(side=LEFT)
        intervalFrame.pack(side=TOP)

        self.inputs = [input1, input2, input3, intervalInput1, intervalInput2, accuracyInput]

    def clear(self):
        for input in self.inputs:
            input.delete(0, END)
        self.resultLabel.destroy()

    def setFirstMethod(self):
        self.method = "Половинное деление"

    def setSecondMethod(self):
        self.method = "Хорды"

    def setThirdMethod(self):
        self.method = "Ньютон"

    def getInterval(self):
        interval = [int(self.inputs[3].get()), int(self.inputs[4].get())]
        return interval

    def getCoefficients(self):
        coefficients = []
        for i in range(3):
            coefficients.append(float(self.inputs[i].get()))

        return coefficients

    def getNolinearEquationResult(self, x):
        return self.coefficients[0] * x * x + self.coefficients[1] * x + self.coefficients[2]

    def getFirstDerivativeResult(self, x):
        return self.coefficients[0] * 2 * x + self.coefficients[1]

    def printResult(self, str):
        self.resultLabel = Label(master=self.window, text=str, font=("Courier", 20))
        self.resultLabel.pack()

    def calculateHalfDiv(self):
        interval = self.getInterval()
        accuracy = 1
        while(accuracy > float(self.inputs[5].get())):
            c = (interval[0] + interval[1]) / 2
            accuracy = abs(interval[0] - interval[1]) / 2
            if(self.getNolinearEquationResult(interval[0]) * self.getNolinearEquationResult(c) <= 0):
                interval = [interval[0], c]
            else:
                interval = [c, interval[1]]

        for i in interval:
            i = round(i, 7)
        self.printResult("x - " + str(interval))

    def calculateChord(self):
        interval = self.getInterval()
        accuracy = 1
        while (accuracy > float(self.inputs[5].get())):
            print(interval)
            a = interval[0]
            b = interval[1]
            fa = self.getNolinearEquationResult(a)
            fb = self.getNolinearEquationResult(b)
            c = (a * fb - b * fa) / (b - fa)
            print("c = ", c)
            lastX = interval[0]
            interval = [c, interval[1]]
            accuracy = abs(lastX - c);

        interval[0] = round(interval[0], 7)
        self.printResult("x - " + str(interval[0]))

    def calculateNuyton(self):
        x = self.coefficients[0] * 2
        lastX = x + 1;
        while(abs(lastX - x) > float(self.inputs[5].get())):
            lastX = x
            x = x - (self.getNolinearEquationResult(x) / self.getFirstDerivativeResult(x))
            print(abs(lastX - x))

        x = round(x, 7)
        self.printResult("x = " + str(x))

    def haveSolution(self):
        coef = self.getCoefficients()
        if(coef[1] ** 2 - 4 * coef[0] * coef[2] >= 0):
            return True
        return False

    def calculate(self):
        if (hasattr(self, "resultLabel")):
            self.resultLabel.destroy()

        if(not self.haveSolution()):
            error(errorCodes.NOT_HAVE_SOLUTION)
            return

        self.coefficients = self.getCoefficients()
        if(self.method == "Ньютон"):
            self.calculateNuyton()
        if (self.method == "Хорды"):
            self.calculateChord()
        if (self.method == "Половинное деление"):
            self.calculateHalfDiv()

    def onOpen(self):
        ftypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*')]
        fold = filedialog.askopenfilename(filetypes=ftypes)
        try:
            text = self.readFile(fold)
        except FileNotFoundError:
            error(errorCodes.FILE_NOT_FOUND)
            return

        self.coefficients = text.split(" ");

def startLab3():
    window = Tk()
    app = thirdLab(window)
    window.mainloop()
