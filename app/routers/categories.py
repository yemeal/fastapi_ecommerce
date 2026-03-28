from typing import Annotated, Sequence

from fastapi import APIRouter, Path, Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema, CategoryCreate
from app.db_depends import get_db

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
    db: Session = Depends(get_db),
) -> Sequence[CategoryModel]:
    """
    Возвращает список всех категорий товара
    """

    stmt = select(CategoryModel).where(CategoryModel.is_active == True)
    categories = db.scalars(stmt).all()
    return categories


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategorySchema,
)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
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
        parent = db.scalars(stmt).first()
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category does not exist",
            )

    # Создание новой категории
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/{category_id}")
async def update_category(
    category_id: Annotated[int, Path(...)],
):
    """
    Обновляет категорию по её ID.
    """
    return {"message": f"Категория с ID {category_id} обновлена (заглушка)"}


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: Annotated[
        int,
        Path(...),
    ],
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """
    Логически удаляет категорию по её ID, устанавливая is_active=False.
    """

    # Проверка существования активной категории
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id,
        CategoryModel.is_active == True,
    )
    category = db.scalars(stmt).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )

    # Логическое удаление категории (установка is_active=False)
    db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(is_active=False)
    )
    db.commit()

    return {"status": "success", "message": "Category marked as inactive"}
