import sqlite3

con = sqlite3.connect("filmdatabase.db") 
cursor = con.cursor()
 
cursor.execute('SELECT имя, возраст FROM acters')
print(cursor.fetchone())
print(cursor.fetchone())

cursor.execute('SELECT имя, возраст FROM acters')
print(cursor.fetchall())

cursor.execute('SELECT имя, возраст FROM acters')
for row in cursor.fetchall():
    print(row[0], row[1])
#con.commit()
