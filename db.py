import os
import sqlite3
from typing import NamedTuple

conn = sqlite3.connect('sqlite_python.db')
cursor = conn.cursor()


class Note(NamedTuple):
    id: int
    user_id: int
    topic: str
    description: str
    date: str
    file_id: str


class ToDo(NamedTuple):
    id: int
    user_id: int
    description: str


class User(NamedTuple):
    user_id: int
    first_enter: str
    user_name: str
    city: str


def insert_new_user(user_id: int, first_enter: str, user_name: str, city: str) -> str:
    sql_insert_query = "insert into users(user_id, first_enter, name, city) values(?, ?, ?, ?)"
    user_data = (user_id, first_enter, user_name, city)
    cursor.execute(sql_insert_query, user_data)
    conn.commit()
    print('новый пользователь сохранен')
    return 'новый пользователь сохранен'


def update_city(user_id: int, city: str):
    query = "update users set city=? where user_id=?"
    cursor.execute(query, (city, user_id))
    conn.commit()


def update_file_note(note_id, file_id):
    query = "update notes set file=? where id=?"
    cursor.execute(query, (file_id, note_id))
    conn.commit()


def get_user_by_user_id(user_id: int) -> User | None:
    get_user_query = "select * from users where user_id = ?"
    cursor.execute(get_user_query, (user_id,))
    user = cursor.fetchall()
    if len(user) != 0:
        user = user[0]
        user = User(user[0], user[1], user[2], user[3])
        print(user)
        return user
    else:
        return None


def convert_to_binary_data(filename):
    print('convert', filename)
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def save_new_note(user_id: int, topic: str, description: str, date_st: str, file_id: str) -> str:
    sql_insert_query = "insert into notes(user_id, topic, description, date, file) values (?, ?, ?, ?, ?)"
    data_tuple = (user_id, topic, description, date_st, file_id)
    cursor.execute(sql_insert_query, data_tuple)
    conn.commit()
    return 'заметка сохранена'
    # print('проведена загрузка', file_expansion)


def delete_note_by_note_id(id: int) -> str:
    delete_query = 'delete from notes where id = ?'
    cursor.execute(delete_query, (id,))
    conn.commit()
    return 'заметка удалена'


def write_to_file(data, filepath):
    # print(filepath)
    with open(filepath, 'wb') as file:
        file.write(data)
    # print('сохранен')


def get_from_notes_by_note_id(id: int) -> Note:
    global note
    sql_read_query = "select * from notes where id = ?"
    cursor.execute(sql_read_query, (id,))
    record = cursor.fetchall()

    for row in record:
        note_id, user_id, topic, description, date, file_id = selection_from_note(note)

        note = Note(id=note_id, user_id=user_id, topic=topic, description=description, date=date, file_id=file_id)

    return note


def get_from_notes_by_user_id(user_id: int) -> [Note]:
    sql_query_for_get_notes_by_user_id = "select * from notes where user_id = ?"
    cursor.execute(sql_query_for_get_notes_by_user_id, (user_id,))
    notes = cursor.fetchall()
    return_dict = []
    for note in notes:
        note_id, user_id, topic, description, date, file_id = selection_from_note(note)

        my_note = Note(note_id, user_id, topic, description, date, file_id)

        return_dict.append(my_note)

    return return_dict


def selection_from_note(note: Note) -> ():
    note_id = note[0]
    user_id = note[1]
    topic = note[2]
    description = note[3]
    date = note[4]
    file_id = note[5]

    res = [note_id, user_id, topic, description, date, file_id]
    return tuple(res)


def update_topic(note_id, topic):
    query = "update notes set topic = ? where id = ?"
    cursor.execute(query, (topic, note_id))
    conn.commit()


def update_description(note_id, description):
    query = "update notes set description = ? where id = ?"
    cursor.execute(query, (description, note_id))
    conn.commit()


def update_date(note_id, date):
    query = "update notes set date = ? where id = ?"
    cursor.execute(query, (date, note_id))
    conn.commit()


def get_to_do_list_for_user(user_id) -> list[ToDo]:
    query = "select * from to_do_list where user_id = ?"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    todos = []
    for row in rows:
        todo = ToDo(row[0], row[1], row[2])
        todos.append(todo)
    return todos


def insert_todo(user_id, todo):
    query = "insert into to_do_list(user_id, description) values(?, ?)"
    cursor.execute(query, (user_id, todo))
    conn.commit()


def delete_todo_by_id(id):
    query = "delete from to_do_list where id = ?"
    cursor.execute(query, (id,))
    conn.commit()


def _init_db():
    """инициализация БД"""
    with open("createdb.sql", 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    cursor.execute("SELECT * FROM sqlite_master")
    table_exists = cursor.fetchall()
    # print(table_exists)
    if table_exists:
        return
    _init_db()


check_db_exists()
# insert_to_notes('тестовый топик 4', 382117477, 'тестовое описание', '03.02.2024 9:55', '')
# print(get_from_notes_by_user_id(382117477))
# print(get_from_notes_by_user_id(382117477))
# insert_new_user(123, 'True', 'Slava')
# get_user_by_user_id(12)
