from tkinter import *
from tkinter import filedialog
import string
from errors import errorCodes, error

class secondLab():

    def __init__(self, window):
        super().__init__()
        self.method = "МПИ"
        self.window = window    # родительское окно в методе
        self.initUI()

    def initUI(self):
        self.window.title("МПИ и Зейдель #2")

        mainMenu = Menu(self.window, tearoff=0)    # создаём вкладку в меню
        self.window.config(menu=mainMenu)
        fileMenu = Menu(mainMenu, tearoff=0)       # вкладываем туда кнопки
        fileMenu.add_command(label="Открыть", command=self.onOpen)
        mainMenu.add_cascade(label="Файл", menu=fileMenu)

        buttonsFrame = Frame(master=self.window)
        buttonsFrame.pack(fill=BOTH)
        buttonsFrame.columnconfigure([0, 1, 4, 5], weight=1, minsize=50)
        buttonsFrame.columnconfigure([2, 3], weight=2, minsize=50)
        buttonsFrame.rowconfigure(0, weight=1, minsize=50)
        self.plusButton = Button(text="+", master=buttonsFrame, width=5, command=self.expandMatrix)
        self.plusButton.grid(row=0, column=0)
        self.minusButton = Button(text="-", master=buttonsFrame, width=5, command=self.decreaseMatrix)
        self.minusButton.grid(row=0, column=1)
        self.clearButton = Button(text="Очистить", master=buttonsFrame, width=10, command=self.clearMatrix)
        self.clearButton.grid(row=0, column=2)


        r1 = Radiobutton(buttonsFrame, text="МПИ", variable=self.method, value=0, command=self.setFirstMethod)
        r2 = Radiobutton(buttonsFrame, text="Зейдель", variable=self.method, value=1, command=self.setSecondMethod)
        r1.select()
        r1.grid(row=0, column=4)
        r2.grid(row=0, column=5)

        self.startButton = Button(text="Рассчитать", master=buttonsFrame, width=10, command=self.calculate)
        self.startButton.grid(row=0, column=3)

        self.matrixLength = 3
        self.inputs = []
        self.drawMatrix()

    def calculate(self):
        self.destroyResults()
        matrix = self.getMatrix()
        if (not self.checkEmptyMatrixElems(matrix)):
            error(errorCodes.EMPTY_MATRIX_ELEM)
            return

        if (not self.checkNotDigitMatrixElems(matrix)):
            error(errorCodes.MATRIX_ELEM_IS_NOT_DIGIT)
            return

        # превращаем строки в числа
        for i in range(self.matrixLength):
            for j in range(self.matrixLength + 1):
                matrix[i][j] = float(matrix[i][j])

        if (self.checkZeroRows(matrix)):
            error(errorCodes.ZERO_ROW)
            return

        if (self.checkZeroColumns(matrix)):
            error(errorCodes.ZERO_COLUMN)
            return

        print("Матрица на входе:")
        self.printMatrix(matrix)

        for i in range(self.matrixLength):
            for j in range(self.matrixLength + 1):
                matrix[i][j] = float(matrix[i][j])

        results = [0] * self.matrixLength
        lastResults = [0] * self.matrixLength
        e = 0.001
        isLoop = True;
        iteration = 1
        while(isLoop):
            isLoop = False
            for i in range(self.matrixLength):
                result = matrix[i][self.matrixLength]
                for j in range(self.matrixLength):
                    if(j == i):
                        continue
                    if(self.method == "МПИ"):
                        result -= matrix[i][j] * lastResults[j]
                    if(self.method == "Зейдель"):
                        result -= matrix[i][j] * results[j]
                result /= matrix[i][i]
                results[i] = result
            for i in range(len(results)):
                if(e < abs(results[i] - lastResults[i])):
                    isLoop = True
                lastResults[i] = results[i]
            print("Шаг: ", iteration, ". ", lastResults);
            iteration += 1

        #for i in range(self.matrixLength):
        #    for j in range(self.matrixLength + 1):
        #        matrix[i][j] /= matrix[i][i]

        resultsStr = self.method + "\n"
        for i in range(len(results)):
            resultsStr += string.ascii_lowercase[i] + " = " + str(round(results[i], 5))
            resultsStr += "\n"
        resultsStr += "Погрешность: " + str(e) + "\n Кол-во итераций: " + str(iteration)
        self.resultsFrame = Frame(master=self.window)

        self.resultsFrame.pack()
        self.resultsFrame.columnconfigure(0, minsize=100)
        resultsLabel = Label(text=resultsStr, master=self.resultsFrame, font=("Courier", 20))
        resultsLabel.grid(row=0, column=0, pady=20, sticky="w")

    def setFirstMethod(self):
        self.method = "МПИ"

    def setSecondMethod(self):
        self.method = "Зейдель"

    def isNumber(self, x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    def destroyResults(self):
        if(hasattr(self, "resultsFrame")):
            self.resultsFrame.destroy()

    def checkEmptyMatrixElems(self, matrix):
        for row in range(self.matrixLength):
            for elem in matrix[row]:
                if(elem == ""):
                    return False
        return True

    def checkNotDigitMatrixElems(self, matrix):
        for row in range(self.matrixLength):
            for elem in matrix[row]:
                if(not self.isNumber(elem)):
                    return False
        return True

    def checkZeroRows(self, matrix):
        for row in range(self.matrixLength):
            for column in range(self.matrixLength + 1):
                if(matrix[row][column] != 0):
                    break
                if(column == self.matrixLength):
                    return True
        return False

    def checkZeroColumns(self, matrix):
        for column in range(self.matrixLength + 1):
            for row in range(self.matrixLength + 1):
                if (row == self.matrixLength):
                    return True
                if(matrix[row][column] != 0):
                    break
        return False

    def clearMatrix(self):
        self.destroyResults()
        for input in self.inputs:
            input.delete(0, END)

    def expandMatrix(self):
        self.destroyResults()
        self.destroyMatrix()
        if(self.matrixLength < 9):
            self.matrixLength += 1
        self.drawMatrix()

    def decreaseMatrix(self):
        self.destroyResults()
        self.destroyMatrix()
        if (self.matrixLength > 2):
            self.matrixLength -= 1
        self.drawMatrix()

    # рисуем матрицу определённого размера
    def drawMatrix(self):
        self.matrixFrame = Frame(master=self.window)
        for i in range(self.matrixLength):

            self.matrixFrame.rowconfigure(i, weight=1, minsize=20)
            for j in range(self.matrixLength + 1):
                self.matrixFrame.columnconfigure(j, weight=1, minsize=20)
                input = Entry(master=self.matrixFrame, width=5)
                self.inputs.append(input)
                input.grid(row=i, column=j, padx=10, pady=5)
        self.matrixFrame.pack(fill=BOTH)

    def destroyMatrix(self):
        self.matrixFrame.destroy()
        self.inputs = []

    def getMatrix(self):
        matrix = []
        for i in range(self.matrixLength):
            matrix.append([0] * (self.matrixLength + 1))
            for j in range(self.matrixLength + 1):
                matrix[i][j] = self.inputs[i * (self.matrixLength + 1):i * (self.matrixLength + 1) + (self.matrixLength + 1)][j].get()
        return matrix

    def onOpen(self):
        self.clearMatrix()

        ftypes = [('Текстовые файлы', '*.txt'), ('Все файлы', '*')]
        fold = filedialog.askopenfilename(filetypes=ftypes)
        try:
            text = self.readFile(fold)
        except FileNotFoundError:
            error(errorCodes.FILE_NOT_FOUND)
            return

        # разделяем весь текст через пробел в массив
        matrixElems = text.split(" ")

        # проверка подстроки на число
        for elem in matrixElems:
            if(not self.isNumber(elem)):
                error(errorCodes.MATRIX_ELEM_IS_NOT_DIGIT)
                return

        # проверка матрицы на соотношение
        matrixLength = 1

        while(matrixLength * (matrixLength + 1) < len(matrixElems)):
            matrixLength += 1

        if (not (matrixLength * (matrixLength + 1) == len(matrixElems))):
            error(errorCodes.INVALID_MATRIX_RATIO)
            return

        print("Элементы матрицы", matrixElems)

        # создаём матрицу
        matrix = []
        for i in range(matrixLength):
            matrix.append([0] * (matrixLength + 1))

        # заполняем матрицу из массива элементов
        for i in range(matrixLength):
            matrix[i] = matrixElems[i * (matrixLength + 1):(matrixLength + 1) * (i + 1)]

        # изменяем размер матрицы под файл
        self.destroyMatrix()
        self.matrixLength = matrixLength
        self.drawMatrix()

        # заполняем инпуты
        for i in range (matrixLength):
            for j in range(matrixLength + 1):
                number = (matrixLength + 1) * i + (j + 1)
                self.inputs[number - 1].delete(0, END)
                self.inputs[number - 1].insert(0, matrix[i][j])

        # печатаем матрицу
        self.printMatrix(matrix)

    def readFile(self, filename):
        with open(filename, "r") as f:
            text = f.read()
        return text

    def printMatrix(self, matrix):
        for i in range(self.matrixLength):
            print(matrix[i])


def startLab2():
    window = Tk()
    app = secondLab(window)
    window.mainloop()
