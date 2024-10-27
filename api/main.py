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

@app.post("/users/", response_model=schemas.UserRead)
async def create_item(
    item: schemas.UserCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_user(session, item)

@app.get("/users/", response_model=list[schemas.UserRead])
async def read_items(session: AsyncSession = Depends(get_session)):
    return await crud.get_users(session)
