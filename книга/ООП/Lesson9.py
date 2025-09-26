from tkinter import *
def click():
    L1.configure(text = 'Hello, ' + E.get())
    
window = Tk()
window.geometry('300x300+100+100')
window.title("My first window")

L1 = Label(window, text = 'Привет!')
L1.pack()
    
B = Button(text="Press me!", width=20, height=5, command = click)
B.pack()

E = Entry(window, width=20)
E.pack()

window.mainloop()
