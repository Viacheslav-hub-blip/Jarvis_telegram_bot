import speech_recognition
from typing import Callable
import asyncio


def speech_decorator(func: Callable):
    def wrapper(file_path):
        res = func(file_path)
        return res

    return wrapper


@speech_decorator
async def get_recognized_speech(file_path) -> str:
    return _speech_recognizing_google(file_path)


def _speech_recognizing_google(file_path) -> str:
    sr = speech_recognition.Recognizer()

    with speech_recognition.AudioFile(file_path) as source:
        audio_data = sr.record(source)
        text = sr.recognize_google(audio_data,  language="ru-RU")
        print(text)
    return text


#asyncio.run(get_recognized_speech('__t1706029884.wav'))