from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .products import Product


class User(Base):

    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    role: Mapped[str] = mapped_column(
        default="buyer",
    )  # 'buyer' or 'seller'

    products: Mapped[list["Product"]] = relationship(
        back_populates="seller",
    )
