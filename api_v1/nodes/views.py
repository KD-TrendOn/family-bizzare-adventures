from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Node
from . import crud
from .schemas import NodeBase, NodeCreate, NodeSchemaDB, NodeQuestion, NodeAnswer
from ..storys import crud as cr
router = APIRouter(tags=["Nodes"])


@router.get("/get-node/{story_id}/{parent_id}/{path_id}/", response_model=NodeSchemaDB)
async def get_node(
    story_id: int,
    parent_id: int,
    path_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    is_node = await crud.get_node_instance(session=session, story_id=story_id, parent_id=parent_id, path_id=path_id)
    if is_node is None:
        story = await cr.get_story(session=session, story_id=story_id)
        base_prompt = story.base_prompt
        node_base = crud.create_node_base(story_id=story_id, base_prompt=base_prompt)
        node_in = NodeBase(**node_base.model_dump(), parent_id=parent_id, path_id=path_id)
        node = await crud.create_node(session=session, node_in=node_in)
        return node
    else:
        return is_node


@router.post(
    "/get-reaction/{node_id}",
    response_model=NodeAnswer,
    status_code=status.HTTP_201_CREATED,
)
async def answer_status(
    node_id: int,
    node_answer: NodeQuestion,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    node = await crud.get_node(session=session, node_id=node_id)
    print(node_answer.answer)
    return NodeAnswer(reaction=True)
