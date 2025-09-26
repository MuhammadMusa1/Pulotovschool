import sqlite3
from tkinter import *

def getrow():
    cursor.execute('''SELECT Learner, Class
                   FROM learners                   
                   ORDER BY Class DESC''')
##INNER JOIN teachers
##ON learners.TeacherID = teachers.id
    rows = cursor.fetchall()
    for row in rows:
        text = ''
        for el in row:
            text = text + str(el) + ' '
        LBinfo.insert(END, text)

def addrow():
    s = ''
    s += Eid.get() + ', '
    s += "'" + Elear.get() + "', "
    s += "'" + Eclass.get() + "', "
    s += Eteach.get() + ', '
    s += Esub.get() + ', '
    s += Erat.get() + ', '
    s += Epart.get()
    cursor.execute('''INSERT INTO learners
                   (id, Learner, Class, TeacherID, SubID, Rate, Part)
                   VALUES (''' + s + ')')
    con.commit()

def learners():
    Fstart.grid_remove()
    Fadd.grid(row=2, column=0)

def subjects():
    pass

def teachers():
    pass

def createtables():
    pass
##    cursor.execute('''CREATE TABLE learns (id integer, Learner text, Class text, Teacher text,
##                      Subject text, Rate integer, Part integer)''')
##    cursor.execute('CREATE TABLE teachers (id integer, Teacher text)')
##    cursor.execute('CREATE TABLE subjects (id integer, Subject text)')


#connect BD
con = sqlite3.connect("school.db") 
cursor = con.cursor()

#interface
window = Tk()
window.geometry('600x600+100+100')
window.title("Myschool")

# create menu
M = Menu(window)
Mm = Menu(M)
Mm.add_command(label='Ученики', command=learners)
Mm.add_command(label='Предметы', command=subjects)
Mm.add_command(label='Учителя', command=teachers)
M.add_cascade(label='Таблицы', menu=Mm)
window.configure(menu=M)


##Linfo = Label(window, text = 'Запись')
##Linfo.pack()
LBinfo = Listbox(window, width = 60)
LBinfo.grid(row=0, column=0)
    
Bget = Button(window, text="Получить запись", width=15, height=2, command = getrow)
Bget.grid(row=1, column=0)

# frame start
Fstart = Frame(window, width=200, height=500, background='#F0E68C')
Lstart = Label(Fstart, text='Выбирете таблицу')
Lstart.grid(row=0, column=0, sticky=N)
Bcreatetables = Button(Fstart, text="Создать таблицы",
                       width=15, height=2, command = createtables)
Bcreatetables.grid(row=1, column=0)

# frame for addrow
Fadd = Frame(window, width=200, height=500, background='#F0E68C')
##Fline.grid_columnconfigure(0, minsize=100)
##Fline.grid_rowconfigure(0, minsize=100)
##Fline.grid_rowconfigure(1, minsize=200)

Lid = Label(Fadd, text='ID')
Llear = Label(Fadd, text='Ученик')
Lclass = Label(Fadd, text='Класс')
Lteach = Label(Fadd, text='Учитель')
Lsub = Label(Fadd, text='Предмет')
Lrat = Label(Fadd, text='Оценка')
Lpart = Label(Fadd, text='Четверть')

Eid = Entry(Fadd, width=7)
Elear = Entry(Fadd, width=20)
Eclass = Entry(Fadd, width=10)
Eteach = Entry(Fadd, width=10)
Esub = Entry(Fadd, width=10)
Erat = Entry(Fadd, width=10)
Epart = Entry(Fadd, width=10)

Badd = Button(Fadd, text="Добавить запись", width=13, height=1, command = addrow)

Lid.grid(row=0, column=0, sticky=N)
Llear.grid(row=0, column=1, sticky=N)
Lclass.grid(row=0, column=2, sticky=N)
Lteach.grid(row=0, column=3, sticky=N)
Lsub.grid(row=0, column=4, sticky=N)
Lrat.grid(row=0, column=5, sticky=N)
Lpart.grid(row=0, column=6, sticky=N)

Eid.grid(row=1, column=0, sticky=N)
Elear.grid(row=1, column=1, sticky=N)
Eclass.grid(row=1, column=2, sticky=N)
Eteach.grid(row=1, column=3, sticky=N)
Esub.grid(row=1, column=4, sticky=N)
Erat.grid(row=1, column=5, sticky=N)
Epart.grid(row=1, column=6, sticky=N)

Badd.grid(row=2, column=0)

Fstart.grid(row=2, column=0)
window.mainloop()
