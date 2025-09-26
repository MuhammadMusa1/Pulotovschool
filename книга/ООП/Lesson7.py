from tkinter import *

window = Tk()
window.geometry('300x300+100+100')
window.title("My first window")

B = Button(text="Press me!", width=20, height=5)
B.pack()

window.mainloop()
