from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .node import Node


class Story(Base):
    base_prompt: Mapped[str] = mapped_column(Text ,nullable=False)
    base_node_id: Mapped[int] = mapped_column(nullable=True)
    nodes: Mapped[list["Node"]] = relationship(back_populates="story")