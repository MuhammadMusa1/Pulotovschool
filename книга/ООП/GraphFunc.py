from tkinter import *
typegraph = 0

def parabol():
    global typegraph
    Fline.grid_remove()
    Fparabol.grid(row=0, column=0)
    typegraph = 1

def line():
    global typegraph
    Fparabol.grid_remove()
    Fline.grid(row=0, column=0)
    typegraph = 0

def buildgraph():
    global typegraph
    C.delete("all")
    # axes of coordinates
    C.create_line(10, 620, 620, 620, fill='red', arrow=LAST)
    C.create_line(10, 620, 10, 10, fill='red', arrow=LAST)
    # if graph is line
    if typegraph == 0:
        try:
            k = float(Ek.get())
            bb = int(Eb.get())
        except:
            C.create_text(300, 300, text = 'Неверные параметры', font = "Times 15")
        else:
            if k < 0:
                b = int (- 600 / k)
                t = 0
            else:
                b = int (  600 / k)
                t = 600
            for i in range(0, b):
                x1 = i
                y1 = t - k * i
                x2 = x1 + 1
                y2 = t - k * (i + 1)
                C.create_line(x1+10, y1, x2+10, y2, fill='black')
                if i % 20 == 0:
                    C.create_text(i, 610, text = str(i), font = "Times 5", fill='blue')
                    C.create_text(20, y1, text = str(int(k*i+bb)), font = "Times 5")
    # if graph is parabol            
    elif typegraph == 1:
        try:
            a = float(Ea.get())
            b = int ((600 / a)**0.5)
        except:
            C.create_text(300, 300, text = 'Неверные параметры', font = "Times 15")
        else:
            for i in range (-b, b):
                x1 = 300 + i
                y1 = 600 - a * i * i 
                x2 = x1 + 1
                y2 = 600 - a * (i + 1)**2
                C.create_line(x1, y1, x2, y2, fill='black')
                if i % 20 == 0:
                    C.create_text(300 + i, 590, text = str(i), font = "Times 5")
                    C.create_text(10, y1, text = str(int(a*i*i)), font = "Times 5", fill='blue')
        
    
window = Tk()
window.geometry('840x680+50+20')
window.title("I am drawing")

# create menu
M = Menu(window)
Mm = Menu(M)
Mm.add_command(label='Парабола', command=parabol)
Mm.add_command(label='Прямая', command=line)
M.add_cascade(label='Графики', menu=Mm)
window.configure(menu=M)

# create canvas for draw graph
Fcanvas = Frame(window, width=630, height=630)
C = Canvas(Fcanvas, width=630, height=630, bg='#FFE4B5')
# axes of coordinates
C.create_line(10, 620, 620, 620, fill='red', arrow=LAST)
C.create_line(10, 620, 10, 10, fill='red', arrow=LAST)



# frame for line parameters
Fline = Frame(window, width=200, height=500, background='#F0E68C')
Fline.grid_columnconfigure(0, minsize=100)
Fline.grid_rowconfigure(0, minsize=100)
Fline.grid_rowconfigure(1, minsize=200)

L = Label(Fline, text='Прямая')
Leq = Label(Fline, text='y = kx + b')
Lk = Label(Fline, text='k')
Lb = Label(Fline, text='b')
Ek = Entry(Fline, width=20)
Eb = Entry(Fline, width=20)


# frame for parabol parameters
Fparabol = Frame(window, width=200, height=500, bg='#F0E68C')
Fparabol.grid_columnconfigure(0, minsize=100)
Fparabol.grid_rowconfigure(0, minsize=100)
Fparabol.grid_rowconfigure(1, minsize=200)
Lp = Label(Fparabol, text='Парабола')
Leqp = Label(Fparabol, text='y = ax^2')
La = Label(Fparabol, text='a:')
Ea = Entry(Fparabol, width=20)

# Button
Bgraph = Button(window, text = 'Нарисовать график', command = buildgraph)

# griding of frames
Fcanvas.grid(row=0, column=1)
Fline.grid(row=0, column=0)
Bgraph.grid(row=1, column=0)

#canvas
C.grid(row=0, column=0, sticky=W)

#line
L.grid(row=0, column=0, sticky=N)
Leq.grid(row=1, column=0, sticky=N)
Lk.grid(row=2, column=0, sticky=N)
Ek.grid(row=2, column=1, sticky=N)
Lb.grid(row=3, column=0, sticky=N)
Eb.grid(row=3, column=1, sticky=N)

#parabol
Lp.grid(row=0, column=0, sticky=N)
Leqp.grid(row=1, column=0, sticky=N)
La.grid(row=2, column=0, sticky=N)
Ea.grid(row=2, column=1, sticky=N)


window.mainloop()
