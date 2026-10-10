from dataclasses import dataclass
from app.services.money import money
from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from app.services.discount import (
    DiscountType,
    calculate_discount,
)
from app.services.tax import calculate_tax_for_line





@dataclass(frozen=True)
class Priceline:
    quantity:int
    unit_price:Decimal
    subtotal : Decimal

@dataclass(frozen=True)
class PriceSummary:
    subtotal: Decimal
    discount_total : Decimal
    taxable_subtotal : Decimal
    tax_total : Decimal
    grand_total : Decimal


def calculate_line_subtotal(
        quantity:int,
        unit_price: Decimal,
)-> Priceline:
    if quantity <=0:
        raise ValueError("Quantity must be greater than  Zero")

    if quantity < 0:
        raise ValueError("Unit Price Cannot be Negative")

    subtotal = money(
        Decimal(quantity)*unit_price,
    )    

    return Priceline(
        quantity= quantity,
        unit_price= money(unit_price),
        subtotal=subtotal,
    )

def calculate_grand_total(
        subtotal : Decimal,
        discount_total : Decimal,
        tax_total:Decimal,
) -> Decimal:
    if subtotal <0:
        raise ValueError("Subtotal cannot be negative")

    if discount_total <0 :
        raise ValueError("Discount Cannot be Negative")

    if tax_total < 0 :
        raise ValueError("tax Cannot Be Negative")

    if discount_total > subtotal :
        raise ValueError("Discount cannot exceed subtotal")

    return money(
        subtotal - discount_total +tax_total
    )

@dataclass(frozen=True)
class CheckoutLineInput:
    quantity: int
    unit_price: Decimal
    tax_rate: Decimal


@dataclass(frozen=True)
class CalculatedLine:
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal


@dataclass(frozen=True)
class CheckoutTotals:
    subtotal: Decimal
    discount_total: Decimal
    tax_total: Decimal
    grand_total: Decimal


def calculate_checkout_line(
    item: CheckoutLineInput,
    discount_type: DiscountType | None = None,
    discount_value: Decimal = Decimal("0.00"),
) -> CalculatedLine:
    price_line = calculate_line_subtotal(
        quantity=item.quantity,
        unit_price=item.unit_price,
    )

    if discount_type is None:
        discount_amount = Decimal("0.00")
    else:
        discount_amount = calculate_discount(
            subtotal=price_line.subtotal,
            discount_type=discount_type,
            discount_value=discount_value,
        )

    tax_amount = calculate_tax_for_line(
        line_subtotal=price_line.subtotal,
        discount_amount=discount_amount,
        tax_rate=item.tax_rate,
    )

    total = money(
        price_line.subtotal
        - discount_amount
        + tax_amount
    )

    return CalculatedLine(
        quantity=price_line.quantity,
        unit_price=price_line.unit_price,
        subtotal=price_line.subtotal,
        discount_amount=discount_amount,
        tax_amount=tax_amount,
        total=total,
    )


def calculate_checkout_totals(
    lines: Iterable[CalculatedLine],
) -> CheckoutTotals:
    subtotal = Decimal("0.00")
    discount_total = Decimal("0.00")
    tax_total = Decimal("0.00")

    for line in lines:
        subtotal += line.subtotal
        discount_total += line.discount_amount
        tax_total += line.tax_amount

    subtotal = money(subtotal)
    discount_total = money(discount_total)
    tax_total = money(tax_total)

    grand_total = calculate_grand_total(
        subtotal=subtotal,
        discount_total=discount_total,
        tax_total=tax_total,
    )

    return CheckoutTotals(
        subtotal=subtotal,
        discount_total=discount_total,
        tax_total=tax_total,
        grand_total=grand_total,
    )