from app.database.base import Base
from app.database.models import (
    AuditLog,
    Category,
    Inventory,
    InventoryTransaction,
    Payment,
    Product,
    Sale,
    SaleItem,
    ScannerSession,
    User,
)

target_metadata = Base.metadata