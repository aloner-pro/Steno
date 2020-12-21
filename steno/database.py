import sqlite3 as db

connect = db.connect('data.db')
cursor = connect.cursor()


def new():
    pass


def check():
    pass


# cursor.execute('create table universal (username text, passwd text)')
# cursor.execute("insert into universal values('Sohel Ahmed', 'sohel')")
# connect.commit()
dt = cursor.execute('select * from universal').fetchall()
print(dt)
connect.close()
