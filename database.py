from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)  # noqa: E501
from sqlalchemy.orm import declarative_base

DB_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)  # noqa: E501

Base = declarative_base()
