from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .products import Product


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(50),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
    )

    # Параметр remote_side указывает ORM, какая колонка принадлежит удалённой стороне отношения,
    # то есть стороне, на которую ссылается внешний ключ.
    # В нашем случае remote_side="Category.id" означает что Category.id это колонка родительского объекта,
    # а parent_id колонка дочернего.
    parent: Mapped["Category | None"] = relationship(
        back_populates="children",
        remote_side="Category.id",
    )
    children: Mapped[list["Category"]] = relationship(
        back_populates="parent",
    )
