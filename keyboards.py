from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton
import text
menu_kb = [
    [InlineKeyboardButton(text="Заметки", callback_data=text.callback_notes)],
    [InlineKeyboardButton(text="Список дел", callback_data=text.callback_to_do_list)],
    [InlineKeyboardButton(text="Погода", callback_data=text.callback_weather)],
    [InlineKeyboardButton(text="Новости", callback_data=text.callback_news)],
    [InlineKeyboardButton(text="AI", callback_data=text.callback_ai)],
    [InlineKeyboardButton(text="Настройки", callback_data=text.callback_settings)]
]

settings_kb = [
    [InlineKeyboardButton(text='Город', callback_data=text.callback_user_city)],
               ]

gigiChat_kb = [
    [InlineKeyboardButton(text="сокращение текста", callback_data=text.callback_summarize_text_ai)],
    # [InlineKeyboardButton(text="выделение главной мысли", callback_data="main_idea_of_text")],
    [InlineKeyboardButton(text="выделить содержимое фаила", callback_data=text.callback_text_content_ai)],
    [InlineKeyboardButton(text="выделение текста из аудио", callback_data=text.text_for_audio_input)],
    [InlineKeyboardButton(text="вопрос", callback_data=text.callback_question_ai)],
    [InlineKeyboardButton(text="в меню", callback_data=text.callback_exit_menu_2)]
]


notes_show_or_edit_or_delete_kb_or_create = [
    [InlineKeyboardButton(text='Посмотреть заметки', callback_data=text.callback_show_notes)],
    [InlineKeyboardButton(text='редактировать заметки', callback_data=text.callback_edit_notes)],
    [InlineKeyboardButton(text='удалить заметки', callback_data=text.callback_delete_notes)],
    [InlineKeyboardButton(text='создать заметку', callback_data=text.callback_create_note)],
    [InlineKeyboardButton(text='В меню', callback_data=text.callback_exit_menu_2)],
]

save_or_cansel_note = [
    [InlineKeyboardButton(text='Сохранить заметку', callback_data=text.callback_save_note)],
    [InlineKeyboardButton(text='Удалить заметку', callback_data=text.callback_delete_notes)]
]

edit_note_kb = [
    [InlineKeyboardButton(text='Редактировать тему', callback_data=text.callback_edit_topic_note)],
    [InlineKeyboardButton(text='Редактировать содержание', callback_data=text.callback_edit_description_note)],
    [InlineKeyboardButton(text='Редактировать дату', callback_data=text.callback_edit_date_note)],
    [InlineKeyboardButton(text='Редактировать фаил', callback_data=text.callback_edit_file_note)]
]

edit_note_again_or_exit = [
    [InlineKeyboardButton(text='Продолжить редактирование', callback_data=text.callback_edit_notes)],
    [InlineKeyboardButton(text='Выйти', callback_data=text.callback_exit_menu_2)]
]

todo_list_kb = [
    [InlineKeyboardButton(text='Посмотреть список дел', callback_data=text.callback_show_to_do)],
    [InlineKeyboardButton(text='Добавить', callback_data=text.callback_create_to_do)],
    [InlineKeyboardButton(text='Удалить', callback_data=text.callback_remove_to_do)],
    [InlineKeyboardButton(text='В меню', callback_data=text.callback_exit_menu_2)],
]


save_or_cansel_note = InlineKeyboardMarkup(inline_keyboard=save_or_cansel_note)
menu_kb = InlineKeyboardMarkup(inline_keyboard=menu_kb)
gigiChat_kb = InlineKeyboardMarkup(inline_keyboard=gigiChat_kb)
edit_note_kb = InlineKeyboardMarkup(inline_keyboard=edit_note_kb)
edit_note_again_or_exit = InlineKeyboardMarkup(inline_keyboard=edit_note_again_or_exit)
notes_show_or_edit_or_delete_kb_or_create = InlineKeyboardMarkup(
    inline_keyboard=notes_show_or_edit_or_delete_kb_or_create)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="выйти в меню")]], resize_keyboard=True, one_time_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="выйти в меню", callback_data="menu")]])
todo_list_kb = InlineKeyboardMarkup(inline_keyboard=todo_list_kb)
settings_kb = InlineKeyboardMarkup(inline_keyboard=settings_kb)
