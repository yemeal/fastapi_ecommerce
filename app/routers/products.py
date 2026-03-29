# products.py
from typing import Annotated, Sequence

from fastapi import APIRouter, Path, Depends, HTTPException, status
from mako.util import restore__ast

from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.db_depends import get_db
from app.models import Category as CategoryModel
from app.models.products import Product as ProductModel
from app.schemas import Product as ProductSchema, ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


# Проверка category_id на активность
def _category_exists(category_id: int, db: Session) -> bool:
    if category_id is not None:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category_id,
            CategoryModel.is_active == True,
        )
        category = db.scalars(stmt).first()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or inactive",
            )
    return True


def _product_exists(product_id: int, db: Session) -> bool:
    if product_id is not None:
        stmt = select(ProductModel).where(
            ProductModel.id == product_id,
            ProductModel.is_active == True,
        )
        product = db.scalars(stmt).first()
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or inactive",
            )
    return True


@router.get(
    "/",
    response_model=list[ProductSchema],
)
async def get_all_products(
    db: Session = Depends(get_db),
) -> Sequence[ProductModel]:
    """
    Возвращает список всех товаров.
    """
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    products = db.scalars(stmt).all()
    return products


@router.post(
    "/",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductModel:
    """
    Создаёт новый товар.
    """

    # Проверка category_id на активность
    _category_exists(product.category_id, db)

    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get(
    "/category/{category_id}",
    response_model=list[ProductSchema],
)
async def get_products_by_category(
    category_id: Annotated[int, Path(...)],
    db: Session = Depends(get_db),
) -> Sequence[ProductModel]:
    """
    Возвращает список товаров в указанной категории по её ID.
    """

    _category_exists(category_id, db)

    stmt = select(ProductModel).where(
        ProductModel.category_id == category_id,
        ProductModel.is_active == True,
    )
    products_by_category = db.scalars(stmt).all()
    return products_by_category


@router.get(
    "/{product_id}",
    response_model=ProductSchema,
)
async def get_product(
    product_id: Annotated[int, Path(...)],
    db: Session = Depends(get_db),
) -> ProductModel:
    """
    Возвращает детальную информацию о товаре по его ID.
    """

    _product_exists(product_id, db)

    stmt = select(ProductModel).where(
        ProductModel.id == product_id,
        ProductModel.is_active == True,
    )
    product = db.scalar(stmt)
    return product


@router.put(
    "/{product_id}",
    response_model=ProductSchema,
)
async def update_product(
    product_id: Annotated[int, Path(...)],
    product: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductModel:
    """
    Обновляет товар по его ID.
    """

    _category_exists(product.category_id, db)
    _product_exists(product_id, db)

    stmt = (
        update(ProductModel)
        .where(
            ProductModel.id == product_id,
        )
        .values(**product.model_dump())
    )
    db.execute(stmt)
    db.commit()
    return db.scalar(select(ProductModel).where(ProductModel.id == product_id))

@router.delete("/{product_id}")
async def delete_product(
    product_id: Annotated[int, Path(...)],
):
    """
    Удаляет товар по его ID.
    """
    return {"message": f"Товар {product_id} удалён (заглушка)"}
