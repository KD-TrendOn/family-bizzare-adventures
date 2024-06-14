from langchain_core.pydantic_v1 import BaseModel, Field, validator, ValidationError

class Options(BaseModel):
    options:list[str]
    @validator('options')
    @classmethod
    def must_be_length_four(cls, o:list):
        if len(o) != 4:
            raise ValueError('Должно быть ровно 4 элемента')
        return o

class Binary(BaseModel):
    correctness:bool