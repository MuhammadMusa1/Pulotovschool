from tkinter import *
def click():
    L1.configure(text = 'Hello, ' + E.get())
    
window = Tk()
window.geometry('300x300+100+100')
window.title("My first window")

F1 = Frame(window, borderwidth = 1, relief=GROOVE)
F1.pack(side=LEFT)

F2 = Frame(window, borderwidth = 5, relief=GROOVE)
F2.pack(side=LEFT)

L1 = Label(F1, text = 'Имя')
L2 = Label(F1, text = 'Фамилия!')
L3 = Label(F1, text = 'Отчество!')

L1.pack()
L2.pack()
L3.pack()

    
##B = Button(F1, text="Press me!", width=20, height=5, command = click)
##B.pack()

E1 = Entry(F2, width=20)
E2 = Entry(F2, width=20)
E3 = Entry(F2, width=20)
E1.pack()
E2.pack()
E3.pack()

window.mainloop()
