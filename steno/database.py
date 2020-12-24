import sqlite3 as db
from datetime import date

connect = db.connect('data.db')
cursor = connect.cursor()


def new(name: str, username: str, passwd: str):
    cursor.execute("INSERT INTO initial(NAME, USERNAME, PASSWORD, DATE) VALUES ({0}, {1}, {2}, {})".format(name, username, passwd, date.today()))
    connect.commit()


def output():
    pass


def close():
    connect.close()


dt = cursor.execute('select * from initial').fetchall()
print(dt)

