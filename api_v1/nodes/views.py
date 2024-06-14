from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import NodeBase, NodeCreate, NodeSchemaDB

router = APIRouter(tags=["Nodes"])


@router.get("/get-node/{story_id}/{parent_id}/{path_id}/", response_model=NodeSchemaDB)
async def get_node(
    story_id: int,
    parent_id: int,
    path_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_(session=session, )


@router.post(
    "/",
    response_model=StorySchemaDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_story(
    story_in: StoryBase,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_story(session=session, story_in=story_in)


@router.get("/{story_id}/", response_model=StorySchemaDB)
async def get_story(
    story: StorySchemaDB = Depends(story_by_id),
):
    return story


@router.delete("/{story_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(
    story: Product = Depends(story_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_story(session=session, story=story)
