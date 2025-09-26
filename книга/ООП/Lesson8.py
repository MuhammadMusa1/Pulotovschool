from tkinter import *
def createLabel():
    L1 = Label(window, text = B.cget('width'))
    L1.pack()

def changeLabel():
    L1.config(text = 'Это мой новый текст!')

def bigButton():
    B.config(width=40, height=10)
    
window = Tk()
window.geometry('300x300+100+100')
window.title("My first window")

L1 = Label(window, text = 'Привет!')
L1.pack()
    
B = Button(text="Press me!", width=20, height=5, command = bigButton)
B.pack()

window.mainloop()
