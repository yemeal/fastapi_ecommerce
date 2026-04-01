from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Модель для создания и обновления пользователя.
    Используется в POST и PUT запросах.
    """

    email: Annotated[
        EmailStr,
        Field(
            ...,
            description="Email пользователя",
        ),
    ]
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            description="Пароль (минимум 8 символов)",
        ),
    ]
    role: Annotated[
        str,
        Field(
            default="buyer",
            pattern="^(buyer|seller)$",
            description="Роль: 'buyer' или 'seller'",
        ),
    ]


class User(BaseModel):
    """
    Модель для ответа с данными пользователя.
    Используется в GET-запросах.
    """

    id: Annotated[
        int,
        Field(
            ...,
            description="ID пользователя",
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            ...,
            description="Email пользователя",
        ),
    ]
    is_active: Annotated[
        bool,
        Field(
            ...,
            description="Пользователь мягко удален или нет",
        ),
    ]
    role: Annotated[
        str,
        Field(
            ...,
            description="Роль: 'buyer' или 'seller'",
        ),
    ]

    model_config = ConfigDict(from_attributes=True)
