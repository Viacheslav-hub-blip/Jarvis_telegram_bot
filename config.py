from langchain.chat_models import GigaChat

BOT_TOKEN = '6708878959:AAF3BUDY2Q0TWvuAR4ueZje2kwrQTzY2NVg'
token = 'ZTk3ZjdmYjMtNmMwOC00NGE1LTk0MzktYzA3ZjU4Yzc2YWI3OmY2OGFlMTQ1LTIyNzgtNDIxMC05M2JmLWFhNTFkZjdmYTY1Yw=='

model = GigaChat(credentials=token, verify_ssl_certs=False)
