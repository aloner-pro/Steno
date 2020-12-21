import sqlite3 as db

connect = db.connect('data.db')
cursor = connect.cursor()


def new():
    pass


def check():
    pass


dt = cursor.execute('select * from universal').fetchall()
print(dt)
connect.close()
