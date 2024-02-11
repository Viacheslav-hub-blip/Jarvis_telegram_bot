import io
import os

from aiogram.types import FSInputFile

import speech_regnize
import states
import text
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext
import gigaChat
from states import Generate, Create_Note
from aiogram.types import ReplyKeyboardRemove
import db

import keyboards
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton

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
        db.insert_new_user(user_id, 'False', message.from_user.full_name)
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


"""Handlers для раздела AI"""


@router.callback_query(F.data == 'ai')
async def gigaChat_kb(callback: CallbackQuery):
    """обработка перехода кнопки AI из главного меню
    заменяем главное меню на наше сообщение
    """
    await callback.message.edit_text('возможности AI', reply_markup=keyboards.gigiChat_kb)


@router.callback_query(F.data == "summarize_text")
async def input_summarize_text(callback: CallbackQuery, state: FSMContext):
    """обработка перехола кнопки 'сокращение текста' из клавиатуры возможностей AI
    устанавливаем состояние
    заменяем клавиатуру возможносстей на 'Отправьте текст запроса к нейросети для генерации текста'
    отправляем клавиаутру для выхода
    """
    await state.set_state(Generate.summarize_text)
    await callback.message.edit_text(text.gen_text)
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
    await callback.message.edit_text(text.gen_text)
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
    await callback.message.edit_text(text.text_content)
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
    await callback.message.edit_text(text.text_for_audio_input)
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


"""Handlers для раздела 'заметки' """


@router.callback_query(F.data == 'notes')
async def show_kb_for_show_edit_delete_create_notes(callback: CallbackQuery):
    await callback.message.edit_text(text.text_for_notes_kb,
                                     reply_markup=keyboards.notes_show_or_edit_or_delete_kb_or_create)


@router.callback_query(F.data == 'show_notes')
async def show_notes_for_user(callback: CallbackQuery):
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
    parse = f"Тема: {note.topic}\n" \
            f"Содержание: {note.description}\n" \
            f"Дата: {note.date}"
    return parse


@router.callback_query(F.data == 'create_note')
async def start_create_new_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Тема топика или кнопка для выхода')
    await state.set_state(Create_Note.create_topic)


@router.message(Create_Note.create_topic)
async def create_topic_for_note(message: Message, state: FSMContext):
    await state.update_data(topic_note=message.text)
    await state.set_state(Create_Note.create_description)
    await message.answer('Текст заметки')


@router.message(Create_Note.create_description)
async def create_description_for_note(message: Message, state: FSMContext):
    await state.update_data(desription_note=message.text)
    await state.set_state(Create_Note.create_date)
    await message.answer('Дата: ')


@router.message(Create_Note.create_date)
async def create_date_for_note(message: Message, state: FSMContext):
    await state.update_data(date_note=message.text)
    await state.set_state(Create_Note.create_file)
    await message.answer('Фаил')


@router.message(Create_Note.create_file)
async def create_file_for_note(message: Message, state: FSMContext):
    if message.document != None:
        file_id = message.document.file_id
        await state.update_data(file_id=file_id)
        await state.set_state(Create_Note.save_file)
    else:
        await state.update_data(file_id='-')
        await state.set_state(Create_Note.save_file)
    await message.answer('Подтвердить сохранение', reply_markup=keyboards.save_or_cansel_note)


@router.callback_query(Create_Note.save_file)
async def save_note(callback: CallbackQuery, state: FSMContext):
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


@router.callback_query(F.data == 'delete_notes')
async def show_all_notes_to_delete(callback: CallbackQuery, state: FSMContext):
    all_notes = db.get_from_notes_by_user_id(callback.from_user.id)
    d = {}
    for i in range(len(all_notes)):
        note = all_notes[i]
        print(note)
        file_id = note.file_id
        print(file_id)

        if file_id != '-':
            parse = parse_note(note)
            await callback.message.answer_document(note.file_id, caption=f'Номер заметки: {i}\n' + parse)
        else:
            parse = parse_note(note)
            await callback.message.answer(f'Номер заметки: {i}\n' + parse)

        d[f'{i}'] = note.id
    await state.update_data(d=d)
    await state.set_state(states.Delete_Note.get_number_note)
    await callback.message.answer('Напишите номера заметок для удаления')


@router.message(states.Delete_Note.get_number_note)
async def delete_note_by_number(message: Message, state: FSMContext):
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
