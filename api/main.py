# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from api.database import get_session
from api.models import Item
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup event")
    yield
    print("shutdown event")

app = FastAPI(lifespan=lifespan)

@app.post("/items/", response_model=Item)
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Item).where(Item.id == item_id)
    result = await session.execute(statement)
    item = result.scalars().first()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item
