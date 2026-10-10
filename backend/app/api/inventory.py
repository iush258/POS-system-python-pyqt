from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.inventory import(
    Inventory,
    InventoryTransaction,
    InventoryTransactionType,
)

from app.database.models.product import Product
from app.database.session import get_db
from app.schemas.inventory import (
    InventoryAdjustmentRequest,
    InventoryCorrectRequest,
    InventoryResponse,
    InventoryRestockRequest,
    InventoryReturnRequest,
    InventoryTransactionResponse,
)

from app.security.dependencies import AdminUser, CashierOrAdminUser

router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)

DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]

def get_locked_product(
        product_id:int,
        db:Session,
) -> Product:
    product = db.scalar(
        select(Product).where(
            Product.id == product_id,
            Product.is_active.is_(True),
        )
    )
    if product is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Active Product Not Found",
        )
    return product


def get_or_create_locked_inventory(
        product_id :int ,
        db : Session,
) -> Inventory:
    inventory = db.scalar(
        select(Inventory)
        .where(Inventory.product_id == product_id)
        .with_for_update()
    )

    if inventory is None:
        inventory = Inventory(
            product_id = product_id,
            quantity = 0 ,
            low_stock_threshold =5,
        )
        db.add(inventory)
        db.flush()

    return inventory

@ router.get(
    "",
    response_model=list[InventoryResponse],
)

def list_inventory(
    db:DatabaseSession,
    current_user = CashierOrAdminUser,
) -> list[Inventory]:
    statement = select (Inventory).order_by(
        Inventory.product_id.asc(),
        )
    return list(db.scalars(statement).all())

@router.get(
    "/low-stock",
    response_model=list[InventoryResponse],
)
def list_low_stock(
    db: DatabaseSession,
    current_user: CashierOrAdminUser,
) -> list[Inventory]:
    statement = (
        select(Inventory)
        .where(
            Inventory.quantity <= Inventory.low_stock_threshold,
        )
        .order_by(Inventory.quantity.asc())
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{product_id}",
    response_model=InventoryResponse,
)
def get_inventory(
    product_id: int,
    db: DatabaseSession,
    current_user: CashierOrAdminUser,
) -> Inventory:
    inventory = db.scalar(
        select(Inventory).where(
            Inventory.product_id == product_id,
        )
    )

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found",
        )

    return inventory


@router.post(
    "/{product_id}/restock",
    response_model=InventoryResponse,
)
def restock_inventory(
    product_id: int,
    request: InventoryRestockRequest,
    db: DatabaseSession,
    current_user: AdminUser,
) -> Inventory:
    get_locked_product(product_id, db)

    inventory = get_or_create_locked_inventory(
        product_id,
        db,
    )

    inventory.quantity += request.quantity

    transaction = InventoryTransaction(
        product_id=product_id,
        transaction_type=InventoryTransactionType.RESTOCK,
        quantity_change=request.quantity,
        reason=request.reason,
    )

    db.add(transaction)
    db.commit()
    db.refresh(inventory)

    return inventory


@router.post(
    "/{product_id}/return",
    response_model=InventoryResponse,
)
def return_inventory(
    product_id: int,
    request: InventoryReturnRequest,
    db: DatabaseSession,
    current_user: AdminUser,
) -> Inventory:
    get_locked_product(product_id, db)

    inventory = get_or_create_locked_inventory(
        product_id,
        db,
    )

    inventory.quantity += request.quantity

    transaction = InventoryTransaction(
        product_id=product_id,
        transaction_type=InventoryTransactionType.RETURN,
        quantity_change=request.quantity,
        reason=request.reason,
    )

    db.add(transaction)
    db.commit()
    db.refresh(inventory)

    return inventory


@router.post(
    "/{product_id}/adjust",
    response_model=InventoryResponse,
)
def adjust_inventory(
    product_id: int,
    request: InventoryAdjustmentRequest,
    db: DatabaseSession,
    current_user: AdminUser,
) -> Inventory:
    get_locked_product(product_id, db)

    inventory = get_or_create_locked_inventory(
        product_id,
        db,
    )

    new_quantity = inventory.quantity + request.quantity_change

    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inventory quantity cannot become negative",
        )

    inventory.quantity = new_quantity

    transaction = InventoryTransaction(
        product_id=product_id,
        transaction_type=InventoryTransactionType.ADJUSTMENT,
        quantity_change=request.quantity_change,
        reason=request.reason,
    )

    db.add(transaction)
    db.commit()
    db.refresh(inventory)

    return inventory


@router.post(
    "/{product_id}/correction",
    response_model=InventoryResponse,
)
def correct_inventory(
    product_id: int,
    request: InventoryCorrectRequest,
    db: DatabaseSession,
    current_user: AdminUser,
) -> Inventory:
    get_locked_product(product_id, db)

    inventory = get_or_create_locked_inventory(
        product_id,
        db,
    )

    quantity_change = request.quantity - inventory.quantity
    inventory.quantity = request.quantity

    transaction = InventoryTransaction(
        product_id=product_id,
        transaction_type=InventoryTransactionType.CORRECTION,
        quantity_change=quantity_change,
        reason=request.reason,
    )

    db.add(transaction)
    db.commit()
    db.refresh(inventory)

    return inventory