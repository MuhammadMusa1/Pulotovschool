from tkinter import *

def deleterect():
    C.delete(rect)

def changecolor(event):
    C.itemconfig(rect, fill='#00BFFF')

def increasesize():
    C.scale(rect, C.coords(rect)[0], C.coords(rect)[1], 2, 2)

def reducesize(event):
    C.scale(rect, C.coords(rect)[0], C.coords(rect)[1], 0.5, 0.5)

def changecolorL(event):
    L.config(bg='red')
    
window = Tk()
window.geometry('500x500+100+100')
window.title("I am drawing")



C = Canvas(window, height=400)
C.pack()
C.create_line(10, 10, 200, 100, fill='red')
rect = C.create_rectangle(10, 105, 190, 190,
                   fill='#FF4500', outline='#48D1CC', width=5)

C.tag_bind(rect,'<Button-3>',changecolor)

C.create_oval(200,50, 280, 130, fill='#D2691E', activefill='#191970')

##B = Button(window, text = 'ChangeRect', command = increasesize)
##B.pack(side=BOTTOM)
##B.bind('<Button-3>', reducesize)

L = Label(window, text='Chameleon')
L.pack()
L.bind('<Button-3>', changecolorL)


window.mainloop()
