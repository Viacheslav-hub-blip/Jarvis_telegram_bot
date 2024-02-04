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
    sql_insert_query = "insert into notes(topic, user_id, description, date, file, file_expansion) values (?, ?,?, ?, ?, ?)"
    file_binary = convert_to_binary_data(file_path)
    file_expansion = file_path.split('.')[1]
    data_tuple = (topic, user_id, description, date_st, file_binary, file_expansion)
    cursor.execute(sql_insert_query, data_tuple)
    conn.commit()
    print('проведена загрузка', file_expansion)


def write_to_file(data, filepath):
    with open(filepath, 'wb') as file:
        file.write(data)
    print('сохранен')


def read_from_notes_by_id(id: int) -> Note:
    global note
    sql_read_query = "select * from notes where id = ?"
    cursor.execute(sql_read_query, (id,))
    record = cursor.fetchall()

    for row in record:
        topic = row[2]
        user_id = row[1]
        description = row[3]
        date = row[4]
        file = row[5]
        file_expansion = row[6]

        file_path = f"users_files\{user_id}_{topic}.{file_expansion}"
        write_to_file(file, file_path)

        note = Note(id=row[0], user_id=user_id, topic=topic, description=description, date=date, file_path=file_path,
                    file_expansion=file_expansion)
    print(note)
    cursor.close()
    return note


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
# insert_to_notes('тестовый топик 3', 123456, 'тестовое описание', '03.02.2024 9:55',
#                r'C:\Users\Slav4ik\PycharmProjects\Jarvis_telegram_bot\trash_files\photo_2024-01-18_18-27-09.jpg')
# read_from_notes_by_id(3)

# insert_new_user(123, 'True', 'Slava')
#get_user_by_user_id(12)
