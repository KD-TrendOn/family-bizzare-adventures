from langchain.output_parsers import PydanticOutputParser
from typing import Optional, Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from os import getenv
from .schemas import Options, Binary

load_dotenv()


llm = ChatOpenAI(
        temperature=0.7,
        model="openai/gpt-3.5-turbo-0125",#openai/gpt-4o
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )

better_llm = ChatOpenAI(
        temperature=0.7,
        model="openai/gpt-4o",#openai/gpt-4o
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )

def generate_storyline(base_prompt:str, current_storyline:Optional[str]=None, option_text:Optional[str]=None):
    if current_storyline is None:
        prompt_template = """
    Ты - создатель историй, задача которого придумывать невероятные истории с каверзными загадками и красочными персонажами.
    Твои пользователи это семья, которая собралась как команда чтобы пройти историю которую ты придумаешь.
    Тебе даны начальные инструкции, про что должна быть история и где и как она происходит.
    История должна основываться на начальных инструкциях. Если написано про одно, генерируй про одно. Если про другое то про другое.
    Команда сейчас только начинает свой путь, и на основе начальных инструкций придумай начальную ситуацию в которой они оказались.
    Напиши краткое описание происходящего вокруг и одного игрового персонажа который им повстречался, и загадку которую он им задает для прохождения дальше.
    Напиши задание которое дает персонаж команде чтобы пройти дальше. СОЗДАВАЙ ИСТОРИЮ ПО СЛЕДУЮЩЕМУ ШАБЛОНУ ТОЛЬКО ТО ЧТО ТАМ НАПИСАНО НЕ ПРО ЛЕС А ПРО НАЧАЛЬНЫЕ ИНСТРУКЦИИ:
    Начальные инструкции:
    {base_prompt}
    Твой ответ:
    """
        prompt = PromptTemplate.from_template(template=prompt_template)
        chain = prompt | better_llm | StrOutputParser()
        result = chain.invoke({'base_prompt':base_prompt})
        print(f'base_story {result}')
        return result
    else:
        prompt_template = """
    Ты - создатель историй, задача которого придумывать невероятные истории с каверзными загадками и красочными персонажами.
    Твои пользователи это семья, которая собралась как команда чтобы пройти историю которую ты придумаешь.
    Тебе даны начальные инструкции, про что должна быть история и где и как она происходит.
    Также, тебе дано текущее местонахождение команды и в какой ситуации она находится.
    Команда после прохождения этапа выбрала пойти по определенному пути.
    Например если она находится в темной комнате и они выбрали поискать дверь, то твоя задача рассказать что произошло в результате этого, и кого они встретили на своем пути.
    Напиши краткое описание происходящего вокруг и одного игрового персонажа который им повстречался, и загадку которую он задает команде для прохождения дальше.
    Напиши задание которое дает персонаж команде чтобы пройти дальше.
    Начальные инструкции:
    {base_prompt}

    Текущее нахождение:
    {current_storyline}

    Выбор пути команды:
    {option_text}
    Твой ответ:
    """
        prompt = PromptTemplate.from_template(template=prompt_template)
        chain = prompt | better_llm | StrOutputParser()
        result = chain.invoke({'base_prompt':base_prompt, "current_storyline":current_storyline, 'option_text':option_text})
        print(f'next storyline {result}')
        return result

def generate_background(base_prompt:str, current_storyline:str):
    prompt_template = """
        Ты - Художник, задача которого описать обстановку происходящую в истории, для последующей поставки этого в модель для генерации изображений.
        Команда пользователей находится внутри истории, и они повстречали на своем пути новую ситуацию с персонажем.
        Тебе даны начальные инструкции, про что должна быть история и где и как она происходит.
        Тебе дано краткое описание ситуации и происходящего вокруг и одного игрового персонажа который им повстречался, и возможно его намерения.
        Просто опиши визуально задний фон и этого персонажа. В стилистике которую задал базовый промпт.
        Напиши промпт который будет визуально описывать задний план происходящего на экране с использованием описаний, указаний и деталей, и напиши промпт описывающий положение и изображение персонажа на первом плане. Опиши очень коротко.
        Для персонажа опиши внешность и укажи что он находится на переднем плане и смотрит прямо. Укажи что персонаж должен выделяться от заднего фона. Опиши коротко.
        Например:
        
        Задний план джунгли, зеленые тропические деревья, речка, передний план большой лев, большая грива, острый взгляд

        Создавай промпт в соответствии с примером основываясь на контексте

        Начальные инструкции:
        {base_prompt}

        Текущее нахождение:
        {current_storyline}

        Твой ответ:
    """
    prompt = PromptTemplate.from_template(template=prompt_template)
    chain = prompt | better_llm | StrOutputParser()
    result = chain.invoke({'base_prompt':base_prompt, "current_storyline":current_storyline})
    print(f'background prompt {result}')
    return result

def generate_question(base_prompt:str, current_storyline:str, background:str):
    prompt_template = """
    Ты - оператор истории, и ты решаешь что сейчас скажет игровой персонаж команде, которая участвует в истории.
    Реплика должна идти от первого лица, поэтому не стесняйся использовать междометья.
    Наши герои попали в ситуацию где их встретил персонаж с определенными намерениями.
    Учитывая начальные инструкции к истории, основываясь в основном на описание текущей ситуации и визуальной обстановки, сгенерируй реплику персонажа,
    которая вводит пользователей в курс дела, а в конце обязательно напиши вопрос который персонаж задает команде.
    Вопрос может быть загадкой, математической задачкой, просьбой перевести предложение или написать стих. Тут можно проявить творчество. Разрешено даже использовать ролевую механику и попросить пользователя описать как он будет действовать чтобы преодолеть какую то проблему в зависимости от контекста.
    Загадка должна именно проверять знания.
    Учти что твой текст должен быть короче 60 слов строго.
    Начальные инструкции:
    {base_prompt}

    Текущее нахождение:
    {current_storyline}

    Текущая обстановка:
    {background}
    """
    prompt = PromptTemplate.from_template(template=prompt_template)
    chain = prompt | better_llm | StrOutputParser()
    result = chain.invoke({'base_prompt':base_prompt, "current_storyline":current_storyline, 'background':background})
    print(f'background prompt {result}')
    return result


def generate_name(current_storyline:str):
    prompt_template = """
    Твоя задача основываясь на контексте истории дать прозвище игровому персонажу участвующему в истории.
    Это может быть ео имя или профессия, что больше подойдет для подписи.
    Ответь только прозвищем, не более 11 букв.

    Контекст:
    {current_storyline}
    """
    prompt = PromptTemplate.from_template(template=prompt_template)
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"current_storyline":current_storyline})
    print(f'name {result}')
    return result

def generate_reactions(base_prompt:str, current_storyline:str, question:str):
    result = dict()
    for stat, nazv in [('Команда прошла задание.', 'true'), ("Команда провалила задание. Но игра не закончена.", 'false')]:
        prompt_template = """
        Ты - оператор истории, которому надо решить что произойдет после того как {stat}.
        Игровой Персонаж задал вопрос команде и тебе известно содержание ситуации в которой оказалась команда.
        Твоя задача написать ответ от лица игрового персонажа на это. От первого лица сообщи комментарий по решению задания, и сообщи что персонаж нехотя или со спокойной душой пропускает их дальше.
        Например:
        Я огорчен вашим решением, но все равно дам вам пройти.

        Или

        Прекрасный ответ! Я очень рад что вы догадались что скрывает в себе данная загадка.


        Ты можешь следовать некоторым начальным инструкциям которые пользователи задали в начале.
        Твой ответ должен быть короче 60 слов строго.
        Начальные инструкции:
        {base_prompt}
        
        Контекст:
        {current_storyline}
        
        Вопрос персонажа:
        {question}
        """
        prompt = PromptTemplate.from_template(template=prompt_template)
        chain = prompt | llm | StrOutputParser()
        result[nazv] = chain.invoke({'stat':stat, 'base_prompt':base_prompt,"current_storyline":current_storyline, 'question':question})
    print(f'reactions {result}')
    return result

def generate_options(base_prompt:str, current_storyline:str, background:str, question:str):
    prompt_template="""
    Ты - оператор ролевой истории, квеста, в котором дружная команда пользователей попала в ситуацию с персонажем, и прошла его задание.
    Твоя задача придумать 4 варианта того куда они теперь могут отправиться или что могут сделать.
    Это может быть что то оригинальное, или какое то смелое решение исходя из ситуации. Например если они находятся в комнате с двумя дверьми можно дать варианты
    Осмотреться, Убежать, Открыть правую дверь, открыть левую дверь.
    Это должен быть обычный список из 4 вариантов.
    Генерируй интересные варианты, сообщающие что команда может переместиться, осмотреться, взаимодействовать с пространством.
    Твой ответ должен соответствовать строгому формату и состоять ровно из 4 вариантов выбора пути.
    Каждый вариант ответа должен быть КОРОЧЕ чем 12 символов
    Следуй форматирующим инструкциям:

    {format_instructions}

    Вот ситуация в которой находятся пользователи:

    {current_storyline}

    Вот так выглядит изначальное описание истории и про что она должна быть:

    {base_prompt}

    Вот описание обстановки вокруг:

    {background}

    Вот задание которое смогла решить команда:

    {question}

    Твой ответ:
    """
    prompt = PromptTemplate.from_template(template=prompt_template)
    output_parser = PydanticOutputParser(pydantic_object=Options)
    format_instructions = output_parser.get_format_instructions()
    chain = prompt | better_llm | output_parser

    result = chain.invoke({'format_instructions':format_instructions, "current_storyline":current_storyline, 'base_prompt':base_prompt, 'background':background, 'question':question}).dict()['options']
    print(f'next options {result}')
    return result

def check_answer(current_storyline:str, question:str, answer:str):
    prompt_template = """
    Ты - игровой персонаж который задал вопрос команде пользователей и получил их ответ. Вопросы и ответы могут быть на разные темы и разной формы.
    Твоя задача ответить True или False в специальном формате который будет указан ниже, что будет указывать на то, считаешь ли ты их ответ правильным.
    Будь строг и отвечай True если команда по настоящему постаралась и дала правильный ответ и False для того чтобы показать что твои потребности не удовлетворены.

    Следуй форматирующим инструкциям:

    {format_instructions}

    Вот ситуация в которой находятся пользователи:

    {current_storyline}

    Вот задание которое команда взялась решить:

    {question}

    Вот ответ который они дали:

    {answer}

    Твое решение:
    """
    prompt = PromptTemplate.from_template(template=prompt_template)
    output_parser = PydanticOutputParser(pydantic_object=Binary)
    format_instructions = output_parser.get_format_instructions()
    chain = prompt | better_llm | output_parser

    result = chain.invoke({'format_instructions':format_instructions, "current_storyline":current_storyline, 'question':question, 'answer':answer}).dict()['correctness']
    print(f'answer check {result}')
    return result
