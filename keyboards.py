from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton

menu_kb = [
    [InlineKeyboardButton(text="Заметки", callback_data="notes")],
    [InlineKeyboardButton(text="Список дел", callback_data="to_do_list")],
    [InlineKeyboardButton(text="Погода", callback_data="weather")],
    [InlineKeyboardButton(text="Новости", callback_data="weather")],
    [InlineKeyboardButton(text="AI", callback_data="ai")]
]

gigiChat_kb = [
    [InlineKeyboardButton(text="сокращение текста", callback_data="summarize_text")],
    # [InlineKeyboardButton(text="выделение главной мысли", callback_data="main_idea_of_text")],
    [InlineKeyboardButton(text="выделить содержимое фаила", callback_data="text_content")],
    [InlineKeyboardButton(text="выделение текста из аудио", callback_data="text_from_audio")],
    [InlineKeyboardButton(text="вопрос", callback_data="question")],
    [InlineKeyboardButton(text="в меню", callback_data="выйти в меню")]
]


notes_show_or_edit_or_delete_kb_or_create = [
    [InlineKeyboardButton(text='Посмотреть заметки', callback_data='show_notes')],
    [InlineKeyboardButton(text='редактировать заметки', callback_data='edit_notes')],
    [InlineKeyboardButton(text='удалить заметки', callback_data='delete_notes')],
    [InlineKeyboardButton(text='создать заметку', callback_data='create_note')],
    [InlineKeyboardButton(text='В меню', callback_data='выйти в меню')],
]

save_or_cansel_note = [
    [InlineKeyboardButton(text='Сохранить заметку', callback_data='save_note')],
    [InlineKeyboardButton(text='Удалить заметку', callback_data='delete_note')]
]

edit_note_kb = [
    [InlineKeyboardButton(text='Редактировать тему', callback_data='edit_topic')],
    [InlineKeyboardButton(text='Редактировать содержание', callback_data='edit_description')],
    [InlineKeyboardButton(text='Редактировать дату', callback_data='edit_date')],
    [InlineKeyboardButton(text='Редактировать фаил', callback_data='edit_file')]
]


save_or_cansel_note = InlineKeyboardMarkup(inline_keyboard=save_or_cansel_note)
menu_kb = InlineKeyboardMarkup(inline_keyboard=menu_kb)
gigiChat_kb = InlineKeyboardMarkup(inline_keyboard=gigiChat_kb)
edit_note_kb = InlineKeyboardMarkup(inline_keyboard=edit_note_kb)
notes_show_or_edit_or_delete_kb_or_create = InlineKeyboardMarkup(
    inline_keyboard=notes_show_or_edit_or_delete_kb_or_create)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="выйти в меню")]], resize_keyboard=True, one_time_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="выйти в меню", callback_data="menu")]])
