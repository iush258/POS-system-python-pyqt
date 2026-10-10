from decimal import Decimal
from enum import Enum

from app.services.money import money


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


def calculate_discount(
    subtotal: Decimal,
    discount_type: DiscountType,
    discount_value: Decimal,
) -> Decimal:
    if subtotal < 0:
        raise ValueError(
            "Subtotal cannot be negative",
        )

    if discount_value < 0:
        raise ValueError(
            "Discount value cannot be negative",
        )

    if discount_type is DiscountType.PERCENTAGE:
        if discount_value > 100:
            raise ValueError(
                "Percentage discount cannot exceed 100",
            )

        discount_amount = subtotal * (
            discount_value / Decimal("100")
        )

    elif discount_type is DiscountType.FIXED:
        discount_amount = discount_value

    else:
        raise ValueError(
            "Unsupported discount type",
        )

    return money(
        min(discount_amount, subtotal),
    )