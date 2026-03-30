# products.py
from typing import Annotated, Sequence

from fastapi import APIRouter, Path, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.db_depends import get_db, get_async_db
from app.models import Category as CategoryModel
from app.models.products import Product as ProductModel
from app.schemas import Product as ProductSchema, ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


# Проверка category_id на активность
async def _category_exists(
    category_id: int,
    db: AsyncSession,
) -> CategoryModel:
    res = await db.scalars(
        select(CategoryModel).where(
            CategoryModel.id == category_id,
            CategoryModel.is_active == True,
        )
    )
    category = res.first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or inactive",
        )
    return category


async def _product_exists(
    product_id: int,
    db: AsyncSession,
) -> ProductModel:
    res = await db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id,
            ProductModel.is_active == True,
        )
    )
    product = res.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )
    return product


@router.get(
    "/",
    response_model=list[ProductSchema],
)
async def get_all_products(
    db: AsyncSession = Depends(get_async_db),
) -> Sequence[ProductModel]:
    """
    Возвращает список всех товаров.
    """
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    products = (await db.scalars(stmt)).all()
    return products


@router.post(
    "/",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
) -> ProductModel:
    """
    Создаёт новый товар.
    """

    # Проверка category_id на активность
    await _category_exists(product.category_id, db)

    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.get(
    "/category/{category_id}",
    response_model=list[ProductSchema],
)
async def get_products_by_category(
    category_id: Annotated[int, Path(...)],
    db: AsyncSession = Depends(get_async_db),
) -> Sequence[ProductModel]:
    """
    Возвращает список товаров в указанной категории по её ID.
    """

    await _category_exists(category_id, db)

    stmt = select(ProductModel).where(
        ProductModel.category_id == category_id,
        ProductModel.is_active == True,
    )
    products_by_category = (await db.scalars(stmt)).all()
    return products_by_category


@router.get(
    "/{product_id}",
    response_model=ProductSchema,
)
async def get_product(
    product_id: Annotated[int, Path(...)],
    db: AsyncSession = Depends(get_async_db),
) -> ProductModel:
    """
    Возвращает детальную информацию о товаре по его ID.
    """

    product = await _product_exists(product_id, db)

    return product


@router.put(
    "/{product_id}",
    response_model=ProductSchema,
)
async def update_product(
    product_id: Annotated[int, Path(...)],
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
) -> ProductModel:
    """
    Обновляет товар по его ID.
    """

    await _category_exists(product.category_id, db)
    await _product_exists(product_id, db)

    stmt = (
        update(ProductModel)
        .where(
            ProductModel.id == product_id,
        )
        .values(**product.model_dump())
    )
    await db.execute(stmt)
    await db.commit()
    return await db.scalar(
        select(ProductModel).where(ProductModel.id == product_id)
    )


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: Annotated[int, Path(...)],
    db: AsyncSession = Depends(get_async_db),
) -> dict[str, str]:
    """
    Удаляет товар по его ID.
    """

    await _product_exists(product_id, db)

    stmt = (
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(is_active=False)
    )
    await db.execute(stmt)
    await db.commit()
    return {"status": "success", "message": "Product marked as inactive"}
