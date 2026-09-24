from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.fastapiauth import DB_URL


class Base(DeclarativeBase):
    pass

engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

async def get_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

