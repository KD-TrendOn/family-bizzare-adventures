from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import StoryRelationMixin

if TYPE_CHECKING:
    from .story import Story

class Node(StoryRelationMixin, Base):
    _story_back_populates = "nodes"

    path_id: Mapped[int] = mapped_column(nullable=True)
    parent_id: Mapped[int] = mapped_column(nullable=True)
    short_line: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    character_name: Mapped[str] = mapped_column(String(40), default="Неизвестный", nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    reaction_true: Mapped[str] = mapped_column(Text, nullable=False)
    reaction_false: Mapped[str] = mapped_column(Text, nullable=False)
    option_one: Mapped[str] = mapped_column(nullable=False)
    option_two: Mapped[str] = mapped_column(nullable=False)
    option_three: Mapped[str] = mapped_column(nullable=False)
    option_four: Mapped[str] = mapped_column(nullable=False)