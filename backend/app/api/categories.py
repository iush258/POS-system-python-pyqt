from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models.category import Category
from app.database.session import get_db
from app.schemas.category import(
    CategoryCreate,
    CategoryResponse,
    CateogruUpdate,
)
from app.security.dependencies import AdminUser , CashierOrAdminUser
router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
)

DatabaseSession = Annotated[
    Session,
    Depends(get_db)
]

@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data:CategoryCreate,
    db: DatabaseSession,
    current_user :AdminUser,
) -> Category:
    existing_category = db.scalar(
        select (Category).where(
            Category.name == category_data.name,
        )
    )

    if existing_category is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=" A Category with this name already exists",
        )
    category = Category(
        name = category_data.name,
        description = category_data.description,
    )
    db.add(category)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= "A Category with this name already Exists"
        ) from None

    db.refresh(category)
    return category

@router.get(
    "",
    response_model=list[CategoryResponse],
)
def list_categories(
    db:DatabaseSession,
    current_user:CashierOrAdminUser,
) -> list[Category]:
    statement = select (Category).order_by(Category.name.asc())
    return list(db.scalars(statement).all())

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)

def get_category(
    category_id :int,
    db:DatabaseSession,
    current_user:CashierOrAdminUser,
) -> Category:
    category = db.scalar(
        select(Category).where(
            Category.id == category_id,
        )
    )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Category Not Found"
        )
    return category

@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id:int,
    category_data:CateogruUpdate,
    db:DatabaseSession,
    current_user : AdminUser,
) -> Category:
    category = db.scalar(
        select (Category).where(
            Category.id == category_id,
        )
    )

    if category is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Category Not Found",
        )

    update_data = category_data.model_dump(
        exclude_unset=True,
    )

    if not update_data:
        return category

    if "name" in update_data:
        duplicate_category = db.scalar(
            select(Category).where(
                Category.name == update_data["name"],
                Category.id == category_id,
            )
        )

        if duplicate_category is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A Category with this name already exists"
            )

    for field_name , field_value in update_data.items():
        setattr(category, field_name, field_value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail="Category update violates a database constraint",
        ) from None

    db.refresh(category)

    return category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id:int,
    db:DatabaseSession,
    current_user : AdminUser,
)-> None:
    category = db.scalar(
        select(Category).where(
            Category.id == category_id,
        )
    )

    if category is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Category not Found"
        )

    db.delete(category)
    db.commit()