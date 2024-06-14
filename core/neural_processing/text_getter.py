from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator, ValidationError
from typing import Optional, Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from os import getenv

load_dotenv()


chat = ChatOpenAI(
        temperature=0.7,
        model="openai/gpt-4o",#openai/gpt-3.5-turbo-0125
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )