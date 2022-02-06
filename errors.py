from tkinter import messagebox as mbox

class errorCodes:
    LAB_NOT_FINED = 1
    FILE_NOT_FOUND = 2
    MATRIX_ELEM_IS_NOT_DIGIT = 3
    INVALID_MATRIX_RATIO = 4
    EMPTY_MATRIX_ELEM = 5
    IDENTIAL_LINES = 6
    ZERO_ROW = 7
    ZERO_COLUMN = 8

def error(errorCode):
    match errorCode:
        case errorCodes.LAB_NOT_FINED:
            mbox.showerror("Ошибка", "Такой лабораторной ещё не придумали(")
        case errorCodes.FILE_NOT_FOUND:
            mbox.showerror("Ошибка", "Файл не найден")
        case errorCodes.MATRIX_ELEM_IS_NOT_DIGIT:
            mbox.showerror("Ошибка", "В матрице есть нечисловой элемент")
        case errorCodes.INVALID_MATRIX_RATIO:
            mbox.showerror("Ошибка", "Неверное соотношение матрицы")
        case errorCodes.EMPTY_MATRIX_ELEM:
            mbox.showerror("Ошибка", "В матрице есть пустой элемент")
        case errorCodes.IDENTIAL_LINES:
            mbox.showerror("Ошибка", "Матрица имеет одинаковые строки, однозначный ответ невозможен")
        case errorCodes.ZERO_ROW:
            mbox.showerror("Ошибка", "Матрица содержит нулевую строку, однозначный ответ невозможен")
        case errorCodes.ZERO_COLUMN:
            mbox.showerror("Ошибка", "Матрица содержит нулевую колонку, однозначный ответ невозможен")
