import tkinter.ttk as ttk
from tkinter import *
#interface
window = Tk()
window.geometry('600x600+100+100')
window.title("Myschool")

# Table for out information
Ttable = ttk.Treeview(window)
Ttable["columns"]=(1,2,3)
Ttable.column("#0", width=50)
Ttable.column(1, width=250)
Ttable.column(2, width=150)
Ttable.column(3, width=80)
Ttable.heading(1, text="Ученик")
Ttable.heading(2, text="Класс")
Ttable.heading(3, text="Оценка")

Ttable.grid(row=0, column=0)
Ttable.insert('',0,text='1', values=('Иванов Иван', '4a', 5))

Ttable1 = ttk.Treeview(window, column=(1,2))
Ttable1.column('#0', width=50)
Ttable1.column(1, width=100)
Ttable1.column(2, width=150)
Ttable1.heading(1, text="Оценка")
Ttable1.grid(row=1, column=0)
Ttable1.insert('',0,text='1', values=('Иванов'))
