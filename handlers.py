import speech_regnize
import states
import text
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext
import gigaChat
from states import Generate, Create_Note
import db
import keyboards
import weather_formatter, weather_api_service

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    user = db.get_user_by_user_id(user_id)
    print(user)

    if user:
        await message.answer(text.text_for_old_user.format(name=message.from_user.full_name),
                             reply_markup=keyboards.menu_kb)
    else:
        db.insert_new_user(user_id, 'False', message.from_user.full_name, 'None')
        await message.answer(text.text_for_new_user.format(name=message.from_user.full_name, user_id=user_id),
                             reply_markup=keyboards.menu_kb)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    """метод для обработки запросов по выходу в меню
    убираем все кнопки в клавиатуре и отправляем главное меню
    """
    await msg.answer(text.transition, reply_markup=ReplyKeyboardRemove())
    await msg.answer(text.menu, reply_markup=keyboards.menu_kb)


@router.callback_query(F.data == "выйти в меню")
async def menu_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text.menu, reply_markup=keyboards.menu_kb)


@router.callback_query(F.data == 'settings')
async def user_settings(callback: CallbackQuery):
    await callback.message.answer('Список настроек', reply_markup=keyboards.settings_kb)


@router.callback_query(F.data == 'user_city')
async def user_city(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите город')
    await state.set_state(states.Edit_city.set_city)


@router.message(states.Edit_city.set_city)
async def set_user_city(message: Message, state: FSMContext):
    db.update_city(message.from_user.id, message.text)
    await state.clear()
    await message.answer("город обновлен", reply_markup=keyboards.menu_kb)


@router.callback_query(F.data == 'weather')
async def weather(callback: CallbackQuery):
    user = db.get_user_by_user_id(callback.from_user.id)
    weather = weather_formatter.format_weather(weather_api_service.get_weather(user.city))
    await callback.message.answer(weather, reply_markup=keyboards.menu_kb)


"""------------------------------------------Handlers для раздела AI---------------------------------------------------"""


@router.callback_query(F.data == 'ai')
async def gigaChat_kb(callback: CallbackQuery):
    """обработка перехода кнопки AI из главного меню
    заменяем главное меню на наше сообщение
    """
    await callback.message.answer('возможности AI', reply_markup=keyboards.gigiChat_kb)


@router.callback_query(F.data == "summarize_text")
async def input_summarize_text(callback: CallbackQuery, state: FSMContext):
    """обработка перехола кнопки 'сокращение текста' из клавиатуры возможностей AI
    устанавливаем состояние
    заменяем клавиатуру возможносстей на 'Отправьте текст запроса к нейросети для генерации текста'
    отправляем клавиаутру для выхода
    """
    await state.set_state(Generate.summarize_text)
    await callback.message.answer(text.gen_text)
    await callback.message.answer(text.gen_exit, reply_markup=keyboards.exit_kb)


@router.message(Generate.summarize_text)
@flags.chat_action("typing")
async def get_summarize_text(message: Message, state: FSMContext):
    """выполняется когда активно состояние 'Generate.summarize_text'
     выделяем текст из сообщения
     отсылаем сообщение 'Пожалуйста, подождите немного...'
     получаем результат от сети
     заменяем сообщение об ожидании на ответ
     """
    text_for_summarize = message.text
    wait_message = await message.answer(text.gen_wait)
    res = await gigaChat.summarize_text(text_for_summarize)
    await wait_message.edit_text(res, disable_web_page_preview=True)


@router.callback_query(F.data == "question")
async def input_question(callback: CallbackQuery, state: FSMContext):
    """обработка кнопки 'вопрос' """
    await state.set_state(Generate.text)
    await callback.message.answer(text.gen_text)
    await callback.message.answer(text.gen_exit, reply_markup=keyboards.exit_kb)


@router.message(Generate.text)
@flags.chat_action("typing")
async def generate_text(message: Message, state: FSMContext):
    """метод для получения ответа на простой вопрос"""
    text_for_AI = message.text
    mesg = await message.answer(text.gen_wait)
    res = await gigaChat.generate_simple_answer(text_for_AI)
    await mesg.edit_text(res, disable_web_page_preview=True)


@router.callback_query(F.data == 'text_content')
async def input_text_for_text_content(callback: CallbackQuery, state: FSMContext):
    """обработка нажатия на кнопку 'выделение содержимого текста' """
    await state.set_state(Generate.text_content)
    await callback.message.answer(text.text_content)
    await callback.message.answer(text.gen_exit, reply_markup=keyboards.exit_kb)


@router.message(Generate.text_content)
@flags.chat_action("typing")
async def generate_content_of_text(message: Message):
    """генерация основного содержимого текста
    сохраняем фаил, передаем путь
    """
    destination = r"C:\Users\Slav4ik\PycharmProjects\Jarvis_telegram_bot\File_for_text_content"
    await message.bot.download(file=message.document.file_id, destination=destination)
    wait_message = await message.answer(text.gen_text)
    answer = await gigaChat.text_content(destination)
    await wait_message.edit_text(answer, disable_web_page_preview=True)


@router.callback_query(F.data == 'text_from_audio')
async def input_audio_for_get_text(callback: CallbackQuery, state: FSMContext):
    """обработка нажатия на кнопку 'выделение текста из аудио' """
    await state.set_state(Generate.text_for_audio)
    await callback.message.answer(text.text_for_audio_input)
    await callback.message.answer(text.gen_exit, reply_markup=keyboards.exit_kb)


@router.message(Generate.text_for_audio)
# @router.message(F.content_type == ContentType.AUDIO)
@flags.chat_action("typing")
async def generate_text_from_audio(message: Message):
    """генерация текста из аудио"""
    destination = r"C:\Users\Slav4ik\PycharmProjects\Jarvis_telegram_bot\File_audio_for_get_text"
    await message.bot.download(file=message.document.file_id, destination=destination)
    wait_message = await message.answer(text.gen_wait)
    text_res = await speech_regnize.get_recognized_speech(destination)
    await wait_message.edit_text(text_res, disable_web_page_preview=True)


"""------------------------------------------заметки, добавление-------------------------------------------------------"""


@router.callback_query(F.data == 'notes')
async def show_kb_for_show_edit_delete_create_notes(callback: CallbackQuery):
    """Показывает возможные действия с заметками"""
    await callback.message.answer(text.text_for_notes_kb,
                                  reply_markup=keyboards.notes_show_or_edit_or_delete_kb_or_create)


@router.callback_query(F.data == 'show_notes')
async def show_notes_for_user(callback: CallbackQuery):
    """Показывает все заметки пользователя
    Если заметок нет, то сразу переход в главное меню
    """
    notes = db.get_from_notes_by_user_id(callback.from_user.id)
    if len(notes) != 0:
        await callback.message.answer('Ваши заметки:')
        for note in notes:
            if note.file_id != '-':
                parse = parse_note(note)
                await callback.message.answer_document(note.file_id, caption=parse)
            else:
                parse = parse_note(note)
                await callback.message.answer(parse)
        await callback.message.answer('Главное меню', reply_markup=keyboards.menu_kb)
    else:
        await callback.message.answer('у вас еще нет заметок')
        await callback.message.answer('Главное меню', reply_markup=keyboards.menu_kb)


def parse_note(note: db.Note) -> str:
    """Парсить заметки"""
    parse = f"Тема: {note.topic}\n" \
            f"Содержание: {note.description}\n" \
            f"Дата: {note.date}"
    return parse


@router.callback_query(F.data == 'create_note')
async def start_create_new_note(callback: CallbackQuery, state: FSMContext):
    """Первое вводное сообщение - ввод темы"""
    await callback.message.answer('Тема топика или кнопка для выхода', reply_markup=keyboards.exit_kb)
    await state.set_state(Create_Note.create_topic)


@router.message(Create_Note.create_topic)
async def create_topic_for_note(message: Message, state: FSMContext):
    """Сохранение темы и предложение ввести текст заметки"""
    await state.update_data(topic_note=message.text)
    await state.set_state(Create_Note.create_description)
    await message.answer('Текст заметки')


@router.message(Create_Note.create_description)
async def create_description_for_note(message: Message, state: FSMContext):
    """Сохранение текста заметки, предложение ввести дату"""
    await state.update_data(desription_note=message.text)
    await state.set_state(Create_Note.create_date)
    await message.answer('Дата: ')


@router.message(Create_Note.create_date)
async def create_date_for_note(message: Message, state: FSMContext):
    """Сохранение даты, предложение добавить фаил"""
    await state.update_data(date_note=message.text)
    await state.set_state(Create_Note.create_file)
    await message.answer('Фаил')


@router.message(Create_Note.create_file)
async def create_file_for_note(message: Message, state: FSMContext):
    """Если существует документ, то добавляем документ. Если сообщение без документа, то ставим - в id документа"""
    if message.document != None:
        file_id = message.document.file_id
        await state.update_data(file_id=file_id)
        await state.set_state(Create_Note.save_note)
    else:
        await state.update_data(file_id='-')
        await state.set_state(Create_Note.save_note)
    await message.answer('Подтвердить сохранение', reply_markup=keyboards.save_or_cansel_note)


@router.callback_query(Create_Note.save_note)
async def save_note(callback: CallbackQuery, state: FSMContext):
    """Сохранение заметки, если была нажата кнопка сохранить, то получаем save_note. Сохраняем заметку"""
    print(callback.data)
    if callback.data == 'save_note':
        user_data = await state.get_data()
        user_id, topic, description, date, file_id = callback.from_user.id, user_data['topic_note'], user_data[
            'desription_note'], user_data['date_note'], user_data['file_id']
        answer = db.save_new_note(user_id, topic, description, date, file_id)
        await callback.message.answer('Заметка сохранена', reply_markup=ReplyKeyboardRemove())
        await menu_callback(callback)
    else:
        await callback.message.answer('Заметка удалена', reply_markup=ReplyKeyboardRemove())
        await menu_callback(callback)
    await state.clear()


"""------------------------------------------Удаление заметок-------------------------------------------------------"""


@router.callback_query(F.data == 'delete_notes')
async def show_all_notes_to_delete(callback: CallbackQuery, state: FSMContext):
    """Показываем все заметки пользователя для дальнейшего удаления. К каждой заметке добавляем номер"""
    all_notes = db.get_from_notes_by_user_id(callback.from_user.id)
    print(callback.from_user.id)
    if len(all_notes) > 0:
        note_dict = await show_notes_add_to_dict(callback, all_notes)
        await state.update_data(d=note_dict)
        await state.set_state(states.Delete_Note.get_number_note)
        await callback.message.answer('Напишите номера заметок для удаления')
    else:
        await callback.message.answer('Заметок еще нет', reply_markup=keyboards.menu_kb)


@router.message(states.Delete_Note.get_number_note)
async def delete_note_by_number(message: Message, state: FSMContext):
    """Удаляем заметки"""
    if len(message.text) > 1:
        numbers = [int(x) for x in message.text.split(',')]
    else:
        numbers = [int(message.text)]
    print(numbers)
    d = await state.get_data()
    d = d['d']
    for num in numbers:
        note_id = d[f'{num}']
        db.delete_note_by_note_id(note_id)

    await message.answer('заметки удалены')
    await menu(message)


"""------------------------------------------------Редактирвоание заметок-----------------------------------------------------"""


async def show_notes_add_to_dict(callback: CallbackQuery, notes) -> dict:
    '''показываем заметки пользователя
    отпраляем два варианта сообщений - с фаилом и без
    формируем словарь - ключь - номер заметки - значение - id
    '''
    d = {}
    for i in range(len(notes)):
        note = notes[i]
        file_id = note.file_id

        if file_id != '-':
            parse = parse_note(note)
            await callback.message.answer_document(note.file_id, caption=f'Номер заметки: {i}\n' + parse)
        else:
            parse = parse_note(note)
            await callback.message.answer(f'Номер заметки: {i + 1}\n' + parse)
        d[f'{i + 1}'] = note.id

    return d


@router.callback_query(F.data == "edit_notes")
async def show_notes_to_edit(callback: CallbackQuery, state: FSMContext):
    """показываем заметик пользователя для редактирования какой то заметки
    показываем все заметки через show_notes
    устанавливаем состояние для ожилания ввода номера заметки
    """
    notes = db.get_from_notes_by_user_id(callback.from_user.id)
    if len(notes) > 0:
        await callback.message.answer('Номер заметки для редактирования')
        dict_note = await show_notes_add_to_dict(callback, notes)
        await state.update_data(d=dict_note)
        await state.set_state(states.Edit_Note.get_number_note)
    else:
        await callback.message.answer('у вас еще нет заметок', reply_markup=keyboards.menu_kb)


@router.message(states.Edit_Note.get_number_note)
async def get_number_note_for_edit(message: Message, state: FSMContext):
    """редактирование заметки
    получаем номер заметки
    по номеру заметки получаем id заметки
    устанавливаем состояние для выбора поля редактирования
    """
    note_number = message.text
    d = await state.get_data()
    d = d['d']
    print('n', d)
    note_id = d[note_number]
    await state.update_data(note_id=note_id)
    await message.answer('Выбери поле для редактирования:', reply_markup=keyboards.edit_note_kb)


@router.callback_query(F.data == 'edit_topic')
async def edit_topic_start(callback: CallbackQuery, state: FSMContext):
    """редактирование заметки
    если было выбрано поле топика заметки
    устанавливаем сотосние на выбор нового раздела
    """
    await callback.message.answer('Введи новый раздел')
    await state.set_state(states.Edit_Note.edit_topic)


@router.message(states.Edit_Note.edit_topic)
async def edit_topic(message: Message, state: FSMContext):
    """редактирование заметки
    получаем и устанавливаем новый топик заметки
    предлагаем выбрать следующее действие
    заканчиваем состояние
    """
    new_topic = message.text
    note_id = (await state.get_data())['note_id']
    db.update_topic(note_id, new_topic)
    await message.answer('Заметка обновлена')
    await message.answer('Выбрать действие:', reply_markup=keyboards.edit_note_again_or_exit)
    await state.clear()


@router.callback_query(F.data == 'edit_description')
async def edit_description_start(callback: CallbackQuery, state: FSMContext):
    """редактирование заметки
    если выбрано редактирование описания
    устанавливаем состояние на ожидание нового описания
    """
    await callback.message.answer("Новое описание")
    await state.set_state(states.Edit_Note.edit_desc)


@router.message(states.Edit_Note.edit_desc)
async def edit_description(message: Message, state: FSMContext):
    """редактирование заметки
    получаем новое описание заметки
    обновляем описание заметки
    """
    desc = message.text
    note_id = (await state.get_data())['note_id']
    db.update_description(note_id, desc)
    await message.answer('Заметка обновлена')
    await message.answer('Выбрать действие:', reply_markup=keyboards.edit_note_again_or_exit)
    await state.clear()


@router.callback_query(F.data == 'edit_date')
async def edit_date_start(callback: CallbackQuery, state: FSMContext):
    """редактирование заметок
    ожидаем новую дату
    """
    await callback.message.answer("Новая дата")
    await state.set_state(states.Edit_Note.edit_date)


@router.message(states.Edit_Note.edit_date)
async def edit_date(message: Message, state: FSMContext):
    """редактирование заметок
    устанавливаем новую дату
    """
    date = message.text
    note_id = (await state.get_data())['note_id']
    db.update_date(note_id, date)
    await message.answer('заметка обновалена', reply_markup=keyboards.edit_note_again_or_exit)
    await state.clear()


@router.callback_query(F.data == 'edit_file')
async def edit_file_start(callback: CallbackQuery, state: FSMContext):
    """редактирование заметок
    ожидаем отправку новго фаила
    """
    await state.set_state(states.Edit_Note.edit_file)
    await callback.message.answer('отправьте новый фаил')


@router.message(states.Edit_Note.edit_file)
async def edit_file(message: Message, state: FSMContext):
    """редактирование заметок
    обновляем фаил заметки
    """
    file = message.document.file_id
    note_id = (await state.get_data())['note_id']
    db.update_file_note(note_id, file)
    await message.answer('заметка обновлена', reply_markup=keyboards.edit_note_again_or_exit)
    await state.clear()


"""------------------------------------------------Список дел-----------------------------------------------------"""


@router.callback_query(F.data == 'to_do_list')
async def todo_options(callback: CallbackQuery):
    """показываем возможности со списком дел"""
    await callback.message.answer('Список дел', reply_markup=keyboards.todo_list_kb)


@router.callback_query(F.data == 'show_todo')
async def show_to_do_list(callback: CallbackQuery):
    """показываем список дел"""
    all_rows = db.get_to_do_list_for_user(callback.from_user.id)
    await callback.message.answer('Список дел на сегодня')
    if len(all_rows) > 0:
        await callback.message.answer(await parse_todo(all_rows), reply_markup=keyboards.todo_list_kb)
    else:
        await callback.message.answer('На сегодня еще нет дел', reply_markup=keyboards.todo_list_kb)


async def parse_todo(todo_list) -> str:
    res = ''
    for i in range(len(todo_list)):
        todo = todo_list[i]
        res += f'{i + 1}. ' \
               f'{todo.description}' \
               f'\n\n'
    return res


@router.callback_query(F.data == 'create_todo')
async def create_todo_start(callback: CallbackQuery, state: FSMContext):
    """создание дела
    ожидаем ввод текста
    """
    await callback.message.answer('текст')
    await state.set_state(states.Create_todo.create_todo)


@router.message(states.Create_todo.create_todo)
async def create_todo(message: Message, state: FSMContext):
    """создание дела
    устанавливаем текст
    """
    db.insert_todo(message.from_user.id, message.text)
    await state.clear()
    await message.answer('добалвено', reply_markup=keyboards.todo_list_kb)


@router.callback_query(F.data == 'remove_todo')
async def remove_todo_start(callback: CallbackQuery, state: FSMContext):
    """удаление дела
    показываем список дел под номерами
    """
    await callback.message.answer('выберите номер для удаления')
    todo_list = db.get_to_do_list_for_user(callback.from_user.id)
    new_list = {}
    res_message = f''
    for i in range(len(todo_list)):
        todo = todo_list[i]
        new_list[f'{i + 1}'] = todo.id
        res_message += f'{i + 1}. {todo.description} \n'
    await state.update_data(todo_list=new_list)
    await state.set_state(states.Remove_todo.get_todo_number)
    await callback.message.answer(res_message)


@router.message(states.Remove_todo.get_todo_number)
async def get_todo_number_for_remove(message: Message, state: FSMContext):
    """удаление дела
    получаем номера дела и удаляем по его id
    """
    numbers = message.text
    todo_ids = (await state.get_data())['todo_list']
    print(todo_ids)
    print(message.text, message.text.split(','))
    if len(numbers) > 1:
        numbers = numbers.split(',')
        for num in numbers:
            id = todo_ids[f'{num}']
            db.delete_todo_by_id(id)
    else:
        db.delete_todo_by_id(todo_ids[f'{numbers}'])

    await state.clear()
    await message.answer('удалено', reply_markup=keyboards.todo_list_kb)
