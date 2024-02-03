from aiogram.client import bot
from aiogram.enums import ContentType

import speech_regnize
import text
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext
import gigaChat
from states import Generate
from aiogram.types import ReplyKeyboardRemove

import keyboards

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=keyboards.menu_kb)


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
