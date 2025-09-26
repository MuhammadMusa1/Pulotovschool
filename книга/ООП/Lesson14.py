from tkinter import *

def go():
    C.move(oval, 1, 0)
    if C.coords(oval)[2] < 290:
        window.after(10, go)
    
window = Tk()
window.geometry('300x200+100+100')
window.title("I am drawing")



C = Canvas(window, width=300, height=150)
C.pack()


oval = C.create_oval(10,50, 60, 100, fill='#D2691E', activefill='#191970')

B = Button(window, text = 'GO', command=go)
B.pack()


window.mainloop()
