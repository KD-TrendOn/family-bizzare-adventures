from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import NodeBase, NodeCreate, NodeSchemaDB, NodeQuestion, NodeAnswer

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
        pass
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
