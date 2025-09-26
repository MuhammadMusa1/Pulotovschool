import sqlite3

conn = sqlite3.connect("filmdatabase.db") 
cursor = conn.cursor()
 
cursor.execute('CREATE TABLE acters (имя text, возраст integer)')
