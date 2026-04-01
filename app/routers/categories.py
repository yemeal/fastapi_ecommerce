from typing import Annotated, Sequence

from fastapi import APIRouter, Path, Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import RoleChecker
from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema, CategoryCreate
from app.db_depends import get_async_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get(
    "/",
    response_model=list[CategorySchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_categories(
    db: AsyncSession = Depends(get_async_db),
) -> Sequence[CategoryModel]:
    """
    Возвращает список всех категорий товара
    """

    stmt = select(CategoryModel).where(CategoryModel.is_active == True)
    categories = await db.scalars(stmt)
    return categories.all()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategorySchema,
    dependencies=[Depends(RoleChecker(roles={"admin"}))],
)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_async_db),
) -> CategoryModel:
    """
    Создаёт новую категорию.
    """

    # Проверка существования parent_id, если указан
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id,
            CategoryModel.is_active == True,
        )
        parent = (await db.scalars(stmt)).first()
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category does not exist",
            )

    # Создание новой категории
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@router.put(
    "/{category_id}",
    response_model=CategorySchema,
    dependencies=[Depends(RoleChecker(roles={"admin"}))],
)
async def update_category(
    category_id: Annotated[
        int,
        Path(...),
    ],
    category: CategoryCreate,
    db: AsyncSession = Depends(get_async_db),
) -> CategoryModel:
    """
    Обновляет категорию по её ID.
    """

    # Проверка существования категории
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id,
        CategoryModel.is_active == True,
    )
    db_category = (await db.scalars(stmt)).first()
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )

    # Проверка существования parent_id, если указан
    if category.parent_id is not None:
        parent_stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id,
            CategoryModel.is_active == True,
        )
        parent = (await db.scalars(parent_stmt)).first()
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category does not exist",
            )
        if parent.id == category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category cannot be its own parent",
            )

    # Обновление категории
    update_data = category.model_dump()
    await db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(**update_data)
    )
    await db.commit()
    return db_category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategorySchema,
    dependencies=[Depends(RoleChecker(roles={"admin"}))],
)
async def delete_category(
    category_id: Annotated[
        int,
        Path(...),
    ],
    db: AsyncSession = Depends(get_async_db),
) -> CategoryModel:
    """
    Логически удаляет категорию по её ID, устанавливая is_active=False.
    """

    # Проверка существования активной категории
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id,
        CategoryModel.is_active == True,
    )
    db_category = (await db.scalars(stmt)).first()
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )

    # Логическое удаление категории (установка is_active=False)
    await db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(is_active=False)
    )
    await db.commit()

    return db_category
