from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .story import Story

class StoryRelationMixin:
    _story_id_nullable: bool = False
    _story_id_unique: bool = False
    _story_back_populates: str | None = None

    @declared_attr
    def story_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("storys.id"),
            unique=cls._story_id_unique,
            nullable=cls._story_id_nullable,
        )

    @declared_attr
    def story(cls) -> Mapped["Story"]:
        return relationship(
            "Story",
            back_populates=cls._story_back_populates,
        )
