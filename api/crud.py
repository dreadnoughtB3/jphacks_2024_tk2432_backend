# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models import Item
from api.schemas import ItemCreate

async def create_item(session: AsyncSession, item: ItemCreate):
    db_item = Item(name=item.name, description=item.description)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def get_items(session: AsyncSession):
    result = await session.execute(select(Item))
    return result.scalars().all()
