from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .dependencies import story_by_id
from .schemas import StorySchemaDB, StoryBase, SendStory
from api_v1.nodes import crud as cr
router = APIRouter(tags=["Storys"])


@router.get("/", response_model=list[StorySchemaDB])
async def get_storys(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_storys(session=session)


@router.post(
    "/",
    response_model=SendStory,
    status_code=status.HTTP_201_CREATED,
)
async def create_story(
    story_in: StoryBase,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    story = await crud.create_story(session=session, story_in=story_in)
    nodebase = cr.create_node_base(story.id, story.base_prompt)
    node = await cr.create_node(session=session, node_in=nodebase)
    story = await crud.update_story(session=session, story_id=story.id, base_node_id=node.id)

    return SendStory(story=story, node=node)


@router.get("/{story_id}/", response_model=SendStory)
async def get_story(
    story: StorySchemaDB = Depends(story_by_id),
):
    return story


@router.delete("/{story_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(
    story: StorySchemaDB = Depends(story_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_story(session=session, story=story)
