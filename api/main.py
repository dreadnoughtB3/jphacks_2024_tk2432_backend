# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import SessionLocal, init_db
from api import crud, models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from api.models import Users
from datetime import datetime, timezone, timedelta
import bcrypt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "wh40k"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@app.post("/users/", response_model=schemas.UserRead)
async def create_user(
    item: schemas.UserCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_user(session, item)


@app.get("/users/", response_model=list[schemas.UserRead])
async def read_users(session: AsyncSession = Depends(get_session)):
    return await crud.get_users(session)


@app.post("/letters/", response_model=schemas.LetterRead)
async def create_letter(
    item: schemas.LetterCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_letter(session, item)


@app.get("/letters/", response_model=list[schemas.LetterRead])
async def read_letters(session: AsyncSession = Depends(get_session)):
    return await crud.get_letters(session)


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await crud.get_user(session)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

