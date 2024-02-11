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
    save_file = State()


class Delete_Note(StatesGroup):
    get_number_note = State()
    delete_note = State()
