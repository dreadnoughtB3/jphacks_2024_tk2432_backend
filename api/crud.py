# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models import Users
from api.schemas import UserCreate

async def create_user(session: AsyncSession, user: UserCreate):
    db_item = Users(name=user.name, description=user.description)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def get_users(session: AsyncSession):
    result = await session.execute(select(Users))
    return result.scalars().all()
