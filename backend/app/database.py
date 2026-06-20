"""
database.py — Async SQLAlchemy database setup
==============================================
Handles Supabase PostgreSQL connection with SSL and pooling.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Build connect args based on environment
connect_args = {"server_settings": {"jit": "off"}}

# Enable SSL for Supabase / production
if settings.DB_SSL:
    connect_args["ssl"] = True

# Disable prepared statements for transaction pooler (port 6543)
if ":6543" in settings.DATABASE_URL:
    connect_args["statement_cache_size"] = 0

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.APP_DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
    connect_args=connect_args,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
