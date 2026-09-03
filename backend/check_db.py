import sqlite3

connection = sqlite3.connect("recoverai.db")

cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

tables = cursor.fetchall()

print("Tables in database:")
print(tables)

connection.close()