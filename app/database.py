from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import IS_DEBUG, DATABASE_URL_POSTGRE, DATABASE_URL_SQLITE

# --------------- Cинхронное подключение к SQLite -------------------------

# Создаём Engine
engine = create_engine(
    DATABASE_URL_SQLITE,
    echo=IS_DEBUG,
)

# Настраиваем фабрику сеансов
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)

# --------------- Асинхронное подключение к PostgreSQL -------------------------
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

# Создаём Engine
async_engine = create_async_engine(
    DATABASE_URL_POSTGRE,
    echo=IS_DEBUG,
)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
