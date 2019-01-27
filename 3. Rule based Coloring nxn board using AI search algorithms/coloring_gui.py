from tkinter import *


def draw(input_array, output):
    master = Tk()

    master.title("William AI Assignment(1b) Output")

    size = 600

    w = Canvas(master, width=size, height=size)
    w.pack(padx=10, pady=10, side=LEFT)

    n = len(input_array[0])

    for i in range(n):
        for j in range(n):
            if input_array[i][j] == 0:
                w.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="blue")
            if input_array[i][j] == 1:
                w.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="red")
            if input_array[i][j] == 2:
                w.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="yellow")
            if input_array[i][j] == 3:
                w.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="green")

    p = Canvas(master, width=size, height=size)
    p.pack(padx=10, pady=10, side=RIGHT)

    for i in range(n):
        for j in range(n):
            if output[i][j] == 0:
                p.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="blue")
            if output[i][j] == 1:
                p.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="red")
            if output[i][j] == 2:
                p.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="yellow")
            if output[i][j] == 3:
                p.create_rectangle(i * size / n, j * size / n, (i * size / n) + size / n, (j * size / n) + size / n,
                                   fill="green")

    mainloop()
