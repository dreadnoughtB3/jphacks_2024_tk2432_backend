# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import SessionLocal, init_db
from api import crud, models, schemas

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.post("/items/", response_model=schemas.ItemRead)
async def create_item(
    item: schemas.ItemCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_item(session, item)

@app.get("/items/", response_model=list[schemas.ItemRead])
async def read_items(session: AsyncSession = Depends(get_session)):
    return await crud.get_items(session)
