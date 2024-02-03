from docx2txt import docx2txt
from langchain.chains import RetrievalQA
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores.faiss import FAISS

from config import model
from langchain.prompts import PromptTemplate
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter

template_for_simple_question = '''
Give the answer so that a five-year-old child understands it.

#QUESTION: {question}
'''

template_for_summarize_text = '''
Please write a one sentence summary of the following text

#TEXT: {text}
'''

template_for_text_content = '''
Please write a one sentence summary of the following text and translate essay on Russian:

    {text}
'''


async def generate_simple_answer(text: str) -> str:
    answer = ''
    try:
        prompt = PromptTemplate(
            input_variables=["question"],
            template=template_for_simple_question
        )
        final_prompt = prompt.format(question=text)
        answer = model.invoke(final_prompt)
        answer = answer.content
    except Exception:
        print('ошибка получения ответа')
    return answer


async def summarize_text(text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template_for_summarize_text
    )

    final_prompt = prompt.format(text=text)
    answer = model.invoke(final_prompt).content

    return answer


async def text_content(document_path: str) -> str:
    with open(document_path, 'r') as file:
        text = docx2txt.process(document_path)

    prompt = PromptTemplate(
        input_variables=["text"],
        template=template_for_text_content
    )

    summary_prompt = prompt.format(text=text)
    # print(summry_prompt)
    output = model.invoke(summary_prompt).content
    return output


#print(asyncio.run(text_content(r"C:\Users\Slav4ik\PycharmProjects\Jarvis_telegram_bot\Текст.docx")))
