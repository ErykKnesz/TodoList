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


def execute_sql(sql, todo=None):
    conn = create_connection()
    cur = conn.cursor()
    if todo:
        cur.execute(sql, todo)
    else:
        cur.execute(sql)
    conn.commit()
    return cur


def boolean_converter(data):
    data.pop('csrf_token')
    if data['done'] is True:
        data['done'] = 'tak'
    else:
        data['done'] = 'nie'
    data = tuple((data for data in data.values()))
    return data


class Todos:
    def __init__(self):
        self.todos = execute_sql(create_todos_sql)

    def all(self):
        sql = "SELECT * FROM todos"
        cur = execute_sql(sql)
        rows = cur.fetchall()
        return rows

    def get(self, id):
        sql = f"SELECT * FROM todos WHERE id = {id}"
        cur = execute_sql(sql)
        row = cur.fetchone()
        return row

    def create(self, data):
        data = boolean_converter(data)
        sql = '''INSERT INTO todos(title, description, done)
             VALUES(?,?,?)'''
        cur = execute_sql(sql, todo=data)
        return cur.lastrowid

    def update(self, id, data):
        boolean_converter(data)
        sql = f"""
            UPDATE todos
            SET title = '{data['title']}',
                description = '{data['description']}',
                done = '{data['done']}'
            WHERE id = {id}"""
        try:
            execute_sql(sql)
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)

    def delete(self, id):
        try:
            sql = f"DELETE FROM todos WHERE id = {id}"
            execute_sql(sql)
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)


todos = Todos()
