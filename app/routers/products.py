# products.py
from typing import Annotated

from fastapi import APIRouter, Path, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.db_depends import get_db
from app.models.products import Product as ProductModel
from app.schemas import Product as ProductSchema, ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get(
    "/",
    response_model=list[ProductSchema],
)
async def get_all_products(
    db: Session = Depends(get_db),
):
    """
    Возвращает список всех товаров.
    """
    stmt = select(ProductModel).order_by(ProductModel.is_active == True)
    products = db.scalars(stmt).all()
    return products


@router.post("/")
async def create_product():
    """
    Создаёт новый товар.
    """
    return {"message": "Товар создан (заглушка)"}


@router.get("/category/{category_id}")
async def get_products_by_category(
    category_id: Annotated[int, Path(...)],
):
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    return {"message": f"Товары в категории {category_id} (заглушка)"}


@router.get("/{product_id}")
async def get_product(
    product_id: Annotated[int, Path(...)],
):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    return {"message": f"Детали товара {product_id} (заглушка)"}


@router.put("/{product_id}")
async def update_product(
    product_id: Annotated[int, Path(...)],
):
    """
    Обновляет товар по его ID.
    """
    return {"message": f"Товар {product_id} обновлён (заглушка)"}


@router.delete("/{product_id}")
async def delete_product(
    product_id: Annotated[int, Path(...)],
):
    """
    Удаляет товар по его ID.
    """
    return {"message": f"Товар {product_id} удалён (заглушка)"}
