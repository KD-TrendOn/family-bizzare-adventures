"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Node, Story
from typing import Optional
from .schemas import NodeCreate, NodeBase

async def get_nodes_of_story(session: AsyncSession, story_id: int) -> list[Node]:
    stmt = select(Node).where(Node.story_id == story_id).order_by(Node.id)
    result: Result = await session.execute(stmt)
    nodes = result.scalars().all()
    return list(nodes)


async def get_node(session: AsyncSession, node_id: int) -> Node | None:
    return await session.get(Node, node_id)




async def create_node(session: AsyncSession, node_in: NodeBase) -> Node:
    node = Node(**node_in.model_dump())
    session.add(node)
    await session.commit()
    # await session.refresh(product)
    return node


async def get_node_instance(session: AsyncSession, path_id: int, parent_id: int, story_id:int) -> Optional[Node]:
    stmt = select(Node).where(Node.story_id == story_id and Node.path_id == path_id, Node.parent_id == parent_id).order_by(Node.id)
    result: Result = await session.execute(stmt)
    node = result.scalars().all()
    nodes = list(node)
    if len(nodes) == 0:
        return None
    return nodes[0]

#hi