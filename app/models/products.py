from decimal import Decimal

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .categories import Category


class Product(Base):
    name: Mapped[str] = mapped_column(
        String(100),
    )
    description: Mapped[str | None] = mapped_column(
        String(500),
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )
    image_url: Mapped[str | None] = mapped_column(
        String(200),
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    stock: Mapped[int]

    category: Mapped["Category"] = relationship(
        back_populates="products",
    )
