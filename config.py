from aiogram.enums import ParseMode
from langchain.chat_models import GigaChat
from aiogram import Bot

BOT_TOKEN = '6708878959:AAF3BUDY2Q0TWvuAR4ueZje2kwrQTzY2NVg'
token = 'ZTk3ZjdmYjMtNmMwOC00NGE1LTk0MzktYzA3ZjU4Yzc2YWI3OmY2OGFlMTQ1LTIyNzgtNDIxMC05M2JmLWFhNTFkZjdmYTY1Yw=='

model = GigaChat(credentials=token, verify_ssl_certs=False)

OPENWEATHER_API = 'af51a693f377695b370d9bd2ce7c7200'

OPENWEATHER_URL = (
    "http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid=" + OPENWEATHER_API
)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)