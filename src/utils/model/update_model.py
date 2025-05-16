from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

# Объявляем TypeVar для разных типов моделей
PydanticUpdate = TypeVar("PydanticUpdate", bound=BaseModel)
DbModel = TypeVar("DbModel", bound=DeclarativeBase)


def create_model(create_data: PydanticUpdate, db_model: DbModel): ...


def update_model(update_data: PydanticUpdate, db_model: DbModel) -> bool:
    """
    Universal function for updating SQLAlchemy models
    based on Pydantic schemas.

    Features:
    1. Works with any SQLAlchemy models that inherit from DeclarativeBase
    2. Updates only the fields explicitly passed in the schema
    3. Supports ID changes through the new_id field
    4. Returns a change flag to control the need for a commit

    Args:
        update_data: Pydantic schema with data for updating
        db_model: Instance of the SQLAlchemy model

    Returns:
        bool: True if there were changes, otherwise False
    """

    changed = False
    update_dict = update_data.model_dump(exclude_unset=True)

    # Обработка специального поля new_id
    if "new_id" in update_dict:
        new_id = update_dict.pop("new_id")
        if new_id is not None and db_model.id != new_id:
            db_model.id = new_id
            changed = True

    # Обновление остальных полей
    for field, value in update_dict.items():
        if field == "id":
            continue  # ID обрабатывается только через new_id

        if value is not None and hasattr(db_model, field):
            current_value = getattr(db_model, field)
            if current_value != value:
                setattr(db_model, field, value)
                changed = True

    return changed
