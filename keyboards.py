from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

menu_kb = [
    [InlineKeyboardButton(text="Зметки", callback_data="notes")],
    [InlineKeyboardButton(text="Список дел", callback_data="to_do_list")],
    [InlineKeyboardButton(text="Погода", callback_data="weather")],
    [InlineKeyboardButton(text="Новости", callback_data="weather")],
    [InlineKeyboardButton(text="AI", callback_data="ai")]
]

gigiChat_kb = [
    [InlineKeyboardButton(text="сокращение текста", callback_data="summarize_text")],
    [InlineKeyboardButton(text="выделение главной мысли", callback_data="main_idea_of_text")],
    [InlineKeyboardButton(text="содержимое текста", callback_data="text_content")],
    [InlineKeyboardButton(text="выделение текста из аудио", callback_data="text_from_audio")],
    [InlineKeyboardButton(text="вопрос", callback_data="question")]
]

menu_kb = InlineKeyboardMarkup(inline_keyboard=menu_kb)
gigiChat_kb = InlineKeyboardMarkup(inline_keyboard=gigiChat_kb)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="выйти в меню", callback_data="menu")]])
