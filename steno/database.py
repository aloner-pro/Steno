import platform
import psutil
import sqlite3 as db
from datetime import date

connect = db.connect('data.db')
cursor = connect.cursor()
info = platform.system() + ' ' + str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + "GB"


def new(name: str, user: str, passwd: str):
    cursor.execute("insert into initial values (?, ?, ?, ?)", (name, user, passwd, date.today()))
    connect.commit()


def format_txt(file: str, passwd: str):
    cursor.execute("insert into user values (?, ?, ?, ?, ?)", ('text', date.today(), file, passwd, info))
    connect.commit()


def format_oth(types: str, file: str):
    cursor.execute("insert into user('FORMAT', 'TIME_STAMP', 'FILE_PATH', 'OS_RAM') VALUES(?, ?, ?, ?)", (types, date.today(), file, info))
    connect.commit()


def close():
    connect.close()


dt = cursor.execute('select * from initial').fetchall()
[print(i) for i in dt]
print('DB- user')
dt2 = cursor.execute('select * from user').fetchall()
[print(k) for k in dt2]
