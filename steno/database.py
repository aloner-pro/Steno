import sqlite3 as db
from datetime import date

connect = db.connect('data.db')
cursor = connect.cursor()


def new(name: str, user: str, passwd: str):
    cursor.execute("insert into initial values (?, ?, ?, ?)", (name, user, passwd, date.today()))
    connect.commit()


def output():
    pass


def close():
    connect.close()


dt = cursor.execute('select * from initial').fetchall()
print(dt)

