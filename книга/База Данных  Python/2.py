import sqlite3

con = sqlite3.connect("filmdatabase.db") 
cursor = con.cursor()
 
cursor.execute('INSERT INTO acters VALUES ("Александр Петров", 31)')
cursor.execute('INSERT INTO acters VALUES ("Джимм Кери", 58)')


con.commit()
