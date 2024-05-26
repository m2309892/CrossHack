from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db.config import config
from sqlalchemy.engine.reflection import Inspector


engine = create_async_engine(
    config.db_url,
    future=True,
    echo=False,
    pool_pre_ping=True
)


class Basic(DeclarativeBase):
    pass


async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Basic.metadata.drop_all)
        await conn.run_sync(Basic.metadata.create_all)
        

async def get_session():
    async with async_session() as session:
        yield session
        