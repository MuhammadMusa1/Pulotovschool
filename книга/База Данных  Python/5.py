import sqlite3
from tkinter import *

def getrow():
    cursor.execute('SELECT имя, возраст FROM acters WHERE возраст<35')
    rows = cursor.fetchall()
    for row in rows:
        text = ''
        for el in row:
            text = text + str(el) + ' '
        LBinfo.insert(END, text)


#connect BD
con = sqlite3.connect("filmdatabase.db") 
cursor = con.cursor()

#interface
window = Tk()
window.geometry('300x300+100+100')
window.title("work with database")


##Linfo = Label(window, text = 'Запись')
##Linfo.pack()
LBinfo = Listbox(window, width = 30)
LBinfo.pack()
    
B = Button(text="Получить запись", width=15, height=2, command = getrow)
B.pack()

window.mainloop()
