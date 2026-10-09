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
from app.database.session import engine


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")