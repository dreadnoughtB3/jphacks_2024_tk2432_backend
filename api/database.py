from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
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
engine = create_async_engine(DATABASE_URL, echo=True)

# セッションを取得するための依存関数
async def get_session():
	async with AsyncSession(engine) as session:
		yield session