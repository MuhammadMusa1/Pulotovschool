from tkinter import *
    
window = Tk()
window.geometry('350x200+100+100')
window.title("My first window")

L1 = Label(window, text = 'Имя:')
L2 = Label(window, text = 'Фамилия:')
L3 = Label(window, text = 'Отчество:')
L4 = Label(window, text = 'Телефон:')

L1.grid(row=0, column=0, sticky=E, pady=5)
L2.grid(row=1, column=0, sticky=E, pady=5)
L3.grid(row=2, column=0, sticky=E, pady=5)
L4.grid(row=3, column=0, sticky=E, pady=5)

B1 = Button(window, text='Помощь', width=7)
B2 = Button(window, text='Отмена', width=7)
B3 = Button(window, text='Принять', width=7)
B1.grid(row=4, column=0, padx=15)
B2.grid(row=4, column=3, sticky=W)
B3.grid(row=4, column=3, padx=5, pady=30, sticky=E)

E1 = Entry(window, width=40)
E2 = Entry(window, width=40)
E3 = Entry(window, width=40)
E4 = Entry(window, width=40)

E1.grid(row=0, column=1, columnspan=3, padx=5, sticky=W)
E2.grid(row=1, column=1, columnspan=3, padx=5, sticky=W)
E3.grid(row=2, column=1, columnspan=3, padx=5, sticky=W)
E4.grid(row=3, column=1, columnspan=3, padx=5, sticky=W)


window.mainloop()
