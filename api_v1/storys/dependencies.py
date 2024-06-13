from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Story

from . import crud

async def story_by_id(
    story_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Story:
    story = await crud.get_story(session=session, story_id=story_id)
    if story is not None:
        return story

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Story {story_id} not found!",
    )
