from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

from src.config import Config

async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def init_db()->None:
    async with async_engine.begin() as conn:        
        from src.db.models import JobApplication # type: ignore[unused-import]
        print(SQLModel.metadata.tables.keys())
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session()-> AsyncGenerator[AsyncSession, None]:
    Session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session