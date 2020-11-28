import sqlite3
from sqlite3 import Error


create_todos_sql = """
-- todos table
CREATE TABLE IF NOT EXISTS todos (
    id integer PRIMARY KEY,
    title text,
    description text,
    done text
);
"""


def create_connection():
    db_file = 'todos.db'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def add_todo(conn, todo):
    sql = '''INSERT INTO todos(title, description, done)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, todo)
    conn.commit()
    return cur.lastrowid


class Todos:
    def __init__(self):
        with open('todos.db', "r") as f:
            conn = create_connection()
            cursor = conn.cursor()
            self.todos = cursor.execute(create_todos_sql)
            conn.close()

    def all(self):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM todos")
        rows = cur.fetchall()
        return rows
    
    def get(self, id):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM todos WHERE id = {id}")
        row = cur.fetchone()
        return row

    def create(self, data):
        data.pop('csrf_token')
        conn = create_connection()
        if data['done'] == True:
            data['done'] = 'tak'
        else:
            data['done'] = 'nie'
        data = tuple((data for data in data.values()))
        add_todo(conn, data)
    
    def update(self, id, data):
        data.pop('csrf_token')
        if data['done'] == True:
            data['done'] = 'tak'
        else:
            data['done'] = 'nie'  
        sql = f"""
            UPDATE todos
            SET title = '{data['title']}',
                description = '{data['description']}',
                done = '{data['done']}'
            WHERE id = {id}"""
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)
    
    def delete(self, id):
        try:
            sql = f"DELETE FROM todos WHERE id = {id}"
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)


todos = Todos()