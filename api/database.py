# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL環境変数が設定されていません。")

# 非同期エンジンの作成
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    }
)

# 非同期セッションの作成
async_session = scoped_session(
                    sessionmaker(
                        autocommit = False,
                        autoflush = False,
                        bind = engine,
                        class_=AsyncSession))   


# セッションを取得するための依存関数
async def get_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
