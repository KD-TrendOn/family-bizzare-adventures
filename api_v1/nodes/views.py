from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Node
from core.neural_processing.text_getter import check_answer
from . import crud
from .schemas import NodeBase, NodeCreate, NodeSchemaDB, NodeQuestion, NodeAnswer, NodeGet
from ..storys import crud as cr
router = APIRouter(tags=["Nodes"])


@router.post("/get-node/", response_model=NodeSchemaDB,status_code=status.HTTP_201_CREATED)
async def get_node(
    data:NodeGet,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    is_node = await crud.get_node_instance(session=session, story_id=data.story_id, parent_id=data.parent_id, path_id=data.path_id)
    if is_node is None:
        story = await cr.get_story(session=session, story_id=data.story_id)
        base_prompt = story.base_prompt
        node_base = await crud.create_node_recursive(session=session, story_id=data.story_id, base_prompt=base_prompt, path_id=data.path_id, parent_id=data.parent_id)
        node = await crud.create_node(session=session, node_in=node_base)
        return node
    else:
        return is_node


@router.post(
    "/get-reaction/",
    response_model=NodeAnswer,
    status_code=status.HTTP_201_CREATED,
)
async def answer_status(
    node_answer: NodeQuestion,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    print('Пришел')
    print(node_answer)
    node = await crud.get_node(session=session, node_id=node_answer.id)
    reaction = check_answer(current_storyline=node.short_line, question=node.question, answer=node_answer.answer)
    return NodeAnswer(reaction=reaction)
