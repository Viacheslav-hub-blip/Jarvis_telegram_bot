from aiogram.filters.state import StatesGroup, State


class Generate(StatesGroup):
    text = State()
    summarize_text = State()
    text_content = State()
    text_for_audio = State()


class Create_Note(StatesGroup):
    create_topic = State()
    create_description = State()
    create_date = State()
    create_file = State()
    save_note = State()


class Delete_Note(StatesGroup):
    get_number_note = State()
    delete_note = State()


class Edit_Note(StatesGroup):
    get_number_note = State()
    edit_topic = State()
    edit_desc = State()
    edit_date = State()
    edit_file = State()


class Create_todo(StatesGroup):
    create_todo = State()


class Remove_todo(StatesGroup):
    get_todo_number = State()


class Edit_city(StatesGroup):
    set_city = State()
