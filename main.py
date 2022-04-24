import tkinter as tk
from errors import errorCodes, error
from lab1 import startLab1
from lab2 import startLab2
from lab3 import startLab3
from lab4 import startLab4
from lab5 import startLab5
from lab6 import startLab6
from lab7 import startLab7
from lab8 import startLab8
from lab9 import startLab9
from lab10 import startLab10
from playsound import playsound
import threading
import math
def playStartSound():
    playsound('trigger.mpeg')

def main():
    x = threading.Thread(target=playStartSound)
    x.start()
    window = tk.Tk()
    window.title("Выч мат от гения")
    columns = 4

    rows = 3
    buttonCommands = [startLab1,
                      startLab2,
                      startLab3,
                      startLab4,
                      startLab5,
                      startLab6,
                      startLab7,
                      startLab8,
                      startLab9,
                      startLab10,
                      lambda er=errorCodes.LAB_NOT_FINED: error(er),
                      lambda er=errorCodes.LAB_NOT_FINED: error(er)]

    for i in range(columns):
        window.columnconfigure(i, weight=1, minsize=75)


        for j in range(rows):
            window.rowconfigure(j, weight=1, minsize=50)
            frame = tk.Frame(master=window)
            frame.grid(row=j, column=i, padx=30, pady=30)
            number = i + j * columns + 1
            button = tk.Button(
                master=frame,
                text="Лабораторная №" + str(number),
                bg="green",
                fg="white",
                height=5,
                command=buttonCommands[number - 1]
            )
            button.pack()

    window.mainloop()


if __name__ == '__main__':
    main()
