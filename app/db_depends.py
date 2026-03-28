from sqlalchemy.orm import Session
from collections.abc import Generator

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Зависимость для получения сессии базы данных.
    Создаёт новую сессию для каждого запроса и закрывает её после обработки.
    """
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        # если где-то начали транзакцию, нужно аккуратно откатить изменения,
        # чтобы освободить блокировки/ресурсы.
        db.rollback()
        raise
    finally:
        db.close()
