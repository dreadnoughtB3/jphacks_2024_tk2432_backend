# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models import Users, Letters
from api.schemas import UserCreate, LetterCreate

async def create_user(session: AsyncSession, user: UserCreate):
    db_item = Users(name=user.name, description=user.description)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def get_users(session: AsyncSession):
    result = await session.execute(select(Users))
    return result.scalars().all()

async def get_user(session: AsyncSession, email: str):
    result = await session.execute(select(Users).where(email == email))
    return result.scaler()

async def create_letter(session: AsyncSession, letter: LetterCreate):
    db_item = Letters(content=letter.content,
                      user_id=letter.user_id,
                      happy=letter.happy,
                      healing=letter.healing,
                      negative=letter.negative,
                      amusing=letter.amusing)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def get_letters(session: AsyncSession):
    result = await session.execute(select(Letters))
    return result.scalars().all()

async def get_letter(session: AsyncSession, id: int):
    result = await session.execute(select(Letters).where(id == id))
    return result.first()