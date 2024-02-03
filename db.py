import os
import sqlite3

conn = sqlite3.connect('sqlite_python.db')
cursor = conn.cursor()


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_to_notes(topic: str, description: str, date_st: str, file_path: str):
    sql_insert_query = "insert into notes(topic, description, date, file) values (?, ?, ?, ?)"
    file_binary = convert_to_binary_data(file_path)
    data_tuple = (topic, description, date_st, file_binary)
    cursor.execute(sql_insert_query, data_tuple)
    conn.commit()
    print('проведена загрузка')
    cursor.close()


def write_to_file(data):
    with open('test.txt', 'w+b') as file:
        file.write(data)
    print('сохранен')


def read_from_notes_by_id(id: int):
    sql_read_query = "select * from notes where id = ?"
    cursor.execute(sql_read_query, (id,))
    record = cursor.fetchall()

    for row in record:
        topic = row[1]
        description = row[2]
        date = row[3]
        file = row[4]
        write_to_file(file)

        print(topic, description, date)
    cursor.close()


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
#insert_to_notes('тестовый топик', 'тестовое описание', '03.02.2024 9:55', 'requirements.txt')
read_from_notes_by_id(1)
