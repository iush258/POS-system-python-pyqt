from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException , Query , status
from sqlalchemy import or_ , select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.models.product import Product
from app.database.session import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)
from app.security.dependencies import AdminUser , CashierOrAdminUser

router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)

DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]



@router.post(
    "",
    response_model=ProductResponse,
    status_code= status.HTTP_201_CREATED,
)

def create_product(
    product_data : ProductCreate,
    db:DatabaseSession,
    current_user: AdminUser,
) -> Product :
    existing_product = db.scalar(
        select (Product).where(
            or_(
                Product.sku == product_data.sku,
                Product.barcode == product_data.barcode,
            )
        )
    )
    if existing_product is not None :
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail="A product with this SKU or barcode already exists",
        )

    product = Product(
        sku=product_data.sku,
        barcode=product_data.barcode,
        name=product_data.name,
        description=product_data.description,
        unit_price=product_data.unit_price,
        tax_rate=product_data.tax_rate,
        category_id=product_data.category_id,
        is_active=True,
    )

    db.add(product)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail="A product with this SKU or barcode already exists",
        ) from None

    db.refresh(product)

    return product



@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products(
    db:DatabaseSession,
    current_user : CashierOrAdminUser,
    search :str | None = Query(
        default= None,
        min_length=1,
        max_length=100,
    ),
    include_inactive : bool = False,
) -> list[Product]:
    statement = select (Product)

    if not include_inactive:
        statement = statement.where(
            Product.is_active.is_(True),
        )

    if search is not None:
        search_pattern = f"%{search}%"
        statement = statement.where(
            or_(
                Product.name.ilike(search_pattern),
                Product.sku.ilike(search_pattern),
                Product.barcode.ilike(search_pattern),
            )
        )
    statement = statement.order_by(Product.name.asc())
    return list(db.scalars(statement).all())



@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)

def get_product(
    product_id : int,
    db : DatabaseSession,
    current_user:CashierOrAdminUser,
) -> Product:
    product = db.scalar(
        select(Product).where(
            Product.id == product_id,
            Product.is_active.is_(True),
        )
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not found"
        )
    return product

@router.get(
    "/barcode/{barcode}",
    response_model=ProductResponse,
)
def get_product_by_barcode(
    barcode:str,
    db: DatabaseSession,
    current_user: CashierOrAdminUser,
) -> Product:
    product = db.scalar(
        select (Product).where(
            Product.barcode == barcode,
            Product.is_active.is_(True),
        )
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active product with this barcode was not found",
        )

    return product


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)

def update_product(
    product_id : int,
    product_data: ProductUpdate,
    db: DatabaseSession,
    current_user : AdminUser,
) -> Product:
    product = db.scalar(
        select(Product).where(
            Product.id == product_id,
        )
    )

    if product is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Product not Found",
        )
    update_data = product_data.model_dump(
        exclude_unset=True,
    )

    if not update_data:
        return product

    if "sku" in update_data:
        update_data.pop("sku")

    if "barcode" in update_data:
        update_data.pop("barcode")

    for field_name, field_value in update_data.items():
        setattr(product,field_name,field_value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product update violates a database constraint",
        ) from None

    db.refresh(product)

    return product



@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)

def deactivate_product(
    product_id:int,
    db:DatabaseSession,
    current_user: AdminUser,
) -> None:
    product = db.scalar(
        select(Product).where(
            Product.id == product_id,
        )
    )
    if product is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Product not Found",
        )
    product.is_active = False
    db.commit()