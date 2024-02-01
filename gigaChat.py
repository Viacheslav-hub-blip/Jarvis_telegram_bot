from config import model
from langchain.prompts import PromptTemplate
import asyncio

template_for_simple_question = '''
Give the answer so that a five-year-old child understands it.

#QUESTION: {question}
'''

template_for_summarize_text = '''
Please write a one sentence summary of the following text

#TEXT: {text}
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

# print(asyncio.run(generate_simple_answer("привет")))
