from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL")
IS_DEBUG: bool = os.getenv("DB_ECHO", "False").lower() == "true"

engine = create_engine(
    DATABASE_URL,
    echo=IS_DEBUG,
)

SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)
