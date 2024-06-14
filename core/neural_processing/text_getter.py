from langchain.output_parsers import PydanticOutputParser
from typing import Optional, Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from os import getenv

load_dotenv()


llm = ChatOpenAI(
        temperature=0.7,
        model="openai/gpt-4o",#openai/gpt-3.5-turbo-0125
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )

def generate_storyline(base_prompt:str, current_storyline:Optional[str]=None, option_text:Optional[str]=None):
    if current_storyline is None:
        prompt_template = """
    Ты - сказочник, задача которого придумывать невероятные истории с каверзными загадками и красочными персонажами.
    Твои пользователи это семья, которая собралась как команда чтобы пройти историю которую ты придумаешь.
    Тебе даны начальные инструкции, про что должна быть история и где и как она происходит.
    Команда сейчас только начинает свой путь, и на основе начальных инструкций придумай начальную ситуацию в которой они оказались.
    Напиши краткое описание происходящего вокруг и одного игрового персонажа который им повстречался, можно описать его намерения.
    Начальные инструкции:
    {base_prompt}
    Твой ответ:
    """
        prompt = PromptTemplate.from_template(template=prompt_template)
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({'base_prompt':base_prompt})
    else:
        prompt_template = """
    Ты - сказочник, задача которого придумывать невероятные истории с каверзными загадками и красочными персонажами.
    Твои пользователи это семья, которая собралась как команда чтобы пройти историю которую ты придумаешь.
    Тебе даны начальные инструкции, про что должна быть история и где и как она происходит.
    Также, тебе дано текущее местонахождение команды и в какой ситуации она находится.
    Команда после прохождения этапа выбрала пойти по определенному пути.
    Например если она находится в темной комнате и они выбрали поискать дверь, то твоя задача рассказать что произошло в результате этого, и кого они встретили на своем пути.
    Напиши краткое описание происходящего вокруг и одного игрового персонажа который им повстречался, можно описать его намерения.
    Начальные инструкции:
    {base_prompt}

    Текущее нахождение:
    {current_storyline}

    Выбор пути команды:
    {option_text}
    Твой ответ:
    """
        prompt = PromptTemplate.from_template(template=prompt_template)
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({'base_prompt':base_prompt, "current_storyline":current_storyline, 'option_text':option_text})

def generate_background(base_prompt:str, current_storyline:str):
    prompt_template = """
        Ты - Художник, задача которого описать обстановку происходящую в истории, для последующей поставки этого в модель для генерации изображений.
        Команда пользователей находится внутри истории, и они повстречали на своем пути новую ситуацию с персонажем.
        Тебе даны начальные инструкции, про что должна быть история и где и как она происходит.
        Тебе дано краткое описание ситуации и происходящего вокруг и одного игрового персонажа который им повстречался, и возможно его намерения.
        Напиши промпт который будет визуально описывать задний план происходящего на экране с использованием описаний и указаний, и напиши промпт описывающий положение и изображение персонажа на первом плане.
        Для персонажа опиши внешность и укажи что он находится на переднем плане и смотрит прямо. Укажи что персонаж должен выделяться от заднего фона.

        Начальные инструкции:
        {base_prompt}

        Текущее нахождение:
        {current_storyline}

        Твой ответ:
    """
    prompt = PromptTemplate.from_template(template=prompt_template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({'base_prompt':base_prompt, "current_storyline":current_storyline})

