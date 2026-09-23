from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from .. import DB_URL


class Base(DeclarativeBase):
    pass

# from ..models.user import User
# from ..models.book import Book

#my_tables = [Book.__table__, User.__table__]

engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

async def get_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

