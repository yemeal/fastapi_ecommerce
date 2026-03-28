from typing import Annotated

from fastapi import APIRouter, Path
from starlette import status

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/")
async def get_all_categories():
    """
    Возвращает список всех категорий товара
    """
    return {"message": "Список всех категорий (заглушка)"}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_category():
    """
    Создаёт новую категорию.
    """
    return {"message": "Категория создана (заглушка)"}


@router.put("/{category_id}")
async def update_category(
    category_id: Annotated[int, Path(...)],
):
    """
    Обновляет категорию по её ID.
    """
    return {"message": f"Категория с ID {category_id} обновлена (заглушка)"}
