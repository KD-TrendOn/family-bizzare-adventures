"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Node
from typing import Optional
from .schemas import NodeCreate, NodeBase 
from core.neural_processing.text_getter import generate_background, generate_name, generate_options, generate_question, generate_reactions, generate_storyline
from core.neural_processing.image_generation import image_generate

def create_node_base(story_id:int, base_prompt:str):
    short_line = generate_storyline(base_prompt)
    image_prompt = generate_background(base_prompt, short_line)
    image = image_generate(image_prompt)
    character_name = generate_name(short_line)
    question = generate_question(base_prompt, short_line, image_prompt)
    reactions = generate_reactions(base_prompt, short_line, question)
    options = generate_options(base_prompt, short_line, image_prompt, question)
    nodebase = NodeBase(
        story_id=story_id,
        short_line=short_line,
        image=image,  # base64 string
        question=question,
        character_name=character_name,
        reaction_true=reactions['true'],
        reaction_false=reactions['false'],
        option_one=options[0],
        option_two=options[1],
        option_three=options[2],
        option_four=options[3]
    )
    return nodebase

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

async def get_node_instance(session: AsyncSession, story_id: int, parent_id: int, path_id: int) -> Optional[Node]:
    stmt = select(Node).where(
        Node.story_id == story_id,
        Node.parent_id == parent_id,
        Node.path_id == path_id
    )
    result: Result = await session.execute(stmt)
    node = result.scalars().first()
    return node
#hi