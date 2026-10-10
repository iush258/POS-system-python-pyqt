from decimal import Decimal

from app.services.discount import DiscountType
from app.services.pricing import (
    CheckoutLineInput,
    calculate_checkout_line,
    calculate_checkout_totals,
)


line = calculate_checkout_line(
    item=CheckoutLineInput(
        quantity=2,
        unit_price=Decimal("100.00"),
        tax_rate=Decimal("5.00"),
    ),
    discount_type=DiscountType.PERCENTAGE,
    discount_value=Decimal("10.00"),
)

totals = calculate_checkout_totals([line])

print(line)
print(totals)