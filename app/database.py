from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

IS_DEBUG: bool = os.getenv("DB_ECHO", "False").lower() == "true"


# --------------- Cинхронное подключение к SQLite -------------------------

# Строка подключения для SQLite
DATABASE_URL_SQLITE: str = os.getenv("DATABASE_URL_SQLITE")

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

DATABASE_URL_POSTGRE: str = os.getenv("DATABASE_URL_POSTGRE")

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
