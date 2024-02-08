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
    file_path: str
    file_expansion: str


class User(NamedTuple):
    user_id: int
    first_enter: str
    user_name: str


def insert_new_user(user_id: int, first_enter: str, user_name: str) -> str:
    sql_insert_query = "insert into users(user_id, first_enter, name) values(?, ?, ?)"
    user_data = (user_id, first_enter, user_name)
    cursor.execute(sql_insert_query, user_data)
    conn.commit()
    print('новый пользователь сохранен')
    return 'новый пользователь сохранен'


def get_user_by_user_id(user_id: int) -> User | None:
    get_user_query = "select * from users where user_id = ?"
    cursor.execute(get_user_query, (user_id,))
    user = cursor.fetchall()
    if len(user) != 0:
        user = user[0]
        user = User(user[0], user[1], user[2])
        print(user)
        return user
    else:
        return None


def convert_to_binary_data(filename):
    print('convert', filename)
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_to_notes(topic: str, user_id: int, description: str, date_st: str, file_path: str):
    sql_insert_query = "insert into notes(topic, user_id, description, date, file.txt, file_expansion) values (?, ?,?, ?, ?, ?)"
    if file_path != '':
        file_binary = convert_to_binary_data(file_path)
        file_expansion = file_path.split('.')[1]
    else:
        file_binary = ''
        file_expansion = ''
    data_tuple = (topic, user_id, description, date_st, file_binary, file_expansion)
    cursor.execute(sql_insert_query, data_tuple)
    conn.commit()
    # print('проведена загрузка', file_expansion)


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
        note_id, user_id, topic, description, date, file_data, file_expansion = selection_from_note(note)
        file_path = ''
        if file_data != '':
            file_path = f"users_files\{user_id}_{topic}.{file_expansion}"
            write_to_file(file_data, file_path)

        note = Note(id=note_id, user_id=user_id, topic=topic, description=description, date=date, file_path=file_path,
                    file_expansion=file_expansion)

    return note


def get_from_notes_by_user_id(user_id: int) -> [Note]:
    sql_query_for_get_notes_by_user_id = "select * from notes where user_id = ?"
    cursor.execute(sql_query_for_get_notes_by_user_id, (user_id,))
    notes = cursor.fetchall()
    return_dict = []
    for note in notes:
        note_id, user_id, topic, description, date, file_data, file_expansion = selection_from_note(note)
        file_path = ''
        if file_data != '':
            file_path = f"users_files/{user_id}_{topic}.{file_expansion}"
            write_to_file(file_data, file_path)

        my_note = Note(note_id, user_id, topic, description, date, file_path, file_expansion)

        return_dict.append(my_note)

    return return_dict


def selection_from_note(note: Note) -> ():
    note_id = note[0]
    user_id = note[1]
    topic = note[2]
    description = note[3]
    date = note[4]
    file_data = note[5]
    file_expansion = note[6]

    res = [note_id, user_id, topic, description, date, file_data, file_expansion]
    return tuple(res)


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
