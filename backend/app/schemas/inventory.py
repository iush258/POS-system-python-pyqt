from datetime import datetime
from enum import Enum
from pydantic import BaseModel , ConfigDict , Field

class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id :int
    product_id:int
    quantity:int
    low_stock_threshold:int


class InventoryTransactionResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id : int
    product_id :int
    transaction_type :int
    quantity_change : int
    reason :str | None
    reference_id : str | None

class InventoryAdjustmentRequest(BaseModel):
    quantity_change : int = Field(
        description= "Positive or Negative Stock Adjustment",
    )
    reason :str = Field(
        min_length=1,
        max_length=255,
    )

class InventoryRestockRequest(BaseModel):
    quantity: int = Field(gt=0)
    reason : str | None = Field(
        default= None,
        max_length=255,
    )

class InventoryReturnRequest(BaseModel):
    quantity: int = Field(gt=0)
    reason : str | None = Field(
        default=None,
        max_length=255,
    )

class InventoryCorrectRequest(BaseModel):
    quantity: int = Field(ge=0)
    reason : str = Field(
        min_length=1,
        max_length=255,
    )