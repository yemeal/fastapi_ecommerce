import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_SQLITE: str = os.getenv("DATABASE_URL_SQLITE")
DATABASE_URL_POSTGRE: str = os.getenv("DATABASE_URL_POSTGRE")
IS_DEBUG: bool = os.getenv("IS_DEBUG", "false").lower() == "true"
SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
