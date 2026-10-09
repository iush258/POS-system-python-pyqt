from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class CheckoutItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CheckoutRequest(BaseModel):
    idempotency_key: str = Field(min_length=10, max_length=255)
    items: list[CheckoutItem] = Field(min_length=1)
    payment_method: Literal["cash", "card", "upi", "other"]
    amount_received: Decimal = Field(gt=0)


class CheckoutResponse(BaseModel):
    sale_id: int
    invoice_number: str
    subtotal: Decimal
    discount_total: Decimal
    tax_total: Decimal
    grand_total: Decimal
    amount_received: Decimal
    change_amount: Decimal