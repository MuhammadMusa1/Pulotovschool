from tkinter import *

def deleterect(event):
    C.delete(rect)

def changecolor(event):
    C.itemconfig(rect, fill='#00BFFF')
    
window = Tk()
window.geometry('300x300+100+100')
window.title("I am drawing")



C = Canvas(window)
C.pack()
C.create_line(10, 10, 200, 100, fill='red')
rect = C.create_rectangle(10, 105, 190, 190,
                   fill='#FF4500', outline='#48D1CC', width=5)

C.tag_bind(rect,'<Button-3>',changecolor)

C.create_oval(200,50, 280, 130, fill='#D2691E', activefill='#191970')

B = Button(window, text = 'DeletRect', command = deleterect)
B.pack()


window.mainloop()
