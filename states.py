from aiogram.fsm.state import StatesGroup, State


class Generate(StatesGroup):
    text = State()
    summarize_text = State()
    text_content = State()
    text_for_audio = State()
