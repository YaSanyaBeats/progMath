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
        self.clearButton = Button(text="Очистить", master=buttonsFrame, width=10)
        self.clearButton.pack(side=LEFT)
        self.startButton = Button(text="Рассчитать", master=buttonsFrame, width=10, command=self.calculate)
        self.startButton.pack(side=LEFT)
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
        Label(master=intervalFrame, text="]").pack(side=LEFT)
        intervalFrame.pack(side=TOP)

        self.inputs = [input1, input2, input3, intervalInput1, intervalInput2]

    def getInterval(self):
        interval = [self.inputs[3], self.inputs[4]]
        return interval

    def getCoefficients(self):
        coefficients = []
        for input in self.inputs:
            coefficients.append(int(input.get()))

        return coefficients

    def getNolinearEquationResult(self, x):
        return self.coefficients[0] * x * x + self.coefficients[1] * x + self.coefficients[2]

    def getFirstDerivativeResult(self, x):
        return self.coefficients[0] * 2 * x + self.coefficients[1]

    def calculate(self):
        self.coefficients = self.getCoefficients()
        x = self.coefficients[0] * 2
        for i in range(5):
            x = x - (self.getNolinearEquationResult(x) / self.getFirstDerivativeResult(x))
        resultStr = "x = " + str(x)
        self.resultLabel = Label(master=self.window, text=resultStr, font=("Courier", 20))
        self.resultLabel.pack()

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
