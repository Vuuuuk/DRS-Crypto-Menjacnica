import pyodbc


def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute("select * from demotb")
    for r in cursor:
        print(f'row ={r}')
    print()


def create(conn):
    print("Create")
    cursor = conn.cursor()
    cursor.execute("insert into demotb(name,age) values(?,?)",("Marijana",40))
    conn.commit()


def update(conn):
    print("Update")
    cursor = conn.cursor()
    cursor.execute("update demotb set name='Ana' where age<20 ")
    conn.commit()


def delete(conn):
    print("Delete")
    cursor = conn.cursor()
    cursor.execute("delete from demotb where name='Marko'")
    conn.commit()


