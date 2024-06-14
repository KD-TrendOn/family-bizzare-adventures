from pydantic import BaseModel, ConfigDict
from typing import Optional


class NodeCreate(BaseModel):
    story_id:int

    path_id:Optional[int] = None

    parent_id: Optional[int] = None


class NodeBase(BaseModel):
    story_id: int

    path_id:Optional[int] = None

    parent_id: Optional[int] = None

    short_line:str

    image:str #base64 string

    question: str

    option_one: str

    option_two: str

    option_three: str

    option_four: str


class NodeSchemaDB(NodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int