"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Story

from .schemas import StoryBase, StorySchemaDB

async def get_storys(session: AsyncSession) -> list[Story]:
    stmt = select(Story).order_by(Story.id)
    result: Result = await session.execute(stmt)
    storys = result.scalars().all()
    return list(storys)


async def get_story(session: AsyncSession, story_id: int) -> Story | None:
    return await session.get(Story, story_id)

async def create_story(session: AsyncSession, story_in: StoryBase) -> Story:
    story = Story(**story_in.model_dump())
    session.add(story)
    await session.commit()
    # await session.refresh(product)
    return story

async def update_story(
        session:AsyncSession,
        story_id:int,
        base_node_id:int        
) -> Story:
    story = await session.get(Story, story_id)
    story.base_node_id = base_node_id
    await session.commit()
    return story

async def delete_story(
    session: AsyncSession,
    story: Story,
    story_update
) -> None:
    await session.delete(story)
    await session.commit()
