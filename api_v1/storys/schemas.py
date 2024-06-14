from pydantic import BaseModel, ConfigDict
from typing import Optional
from ..nodes.schemas import NodeSchemaDB
class StoryBase(BaseModel):
    base_prompt : str = "Придумай совершенно случайную каверзную ситуацию в которой оказалась команда"


class StorySchemaDB(StoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    base_node_id: Optional[int] = None

class SendStory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    story: StorySchemaDB
    base_node: NodeSchemaDB