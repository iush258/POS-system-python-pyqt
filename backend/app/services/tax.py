from decimal import Decimal

from app.services.pricing import money


def calculate_tax_amount(
    taxable_amount: Decimal,
    tax_rate: Decimal,
) -> Decimal:
    if taxable_amount < 0:
        raise ValueError(
            "Taxable amount cannot be negative",
        )

    if tax_rate < 0 or tax_rate > 100:
        raise ValueError(
            "Tax rate must be between 0 and 100",
        )

    tax_amount = taxable_amount * (
        tax_rate / Decimal("100")
    )

    return money(tax_amount)


def calculate_tax_for_line(
    line_subtotal: Decimal,
    discount_amount: Decimal,
    tax_rate: Decimal,
) -> Decimal:
    if discount_amount < 0:
        raise ValueError(
            "Discount cannot be negative",
        )

    if discount_amount > line_subtotal:
        raise ValueError(
            "Discount cannot exceed line subtotal",
        )

    taxable_amount = line_subtotal - discount_amount

    return calculate_tax_amount(
        taxable_amount=taxable_amount,
        tax_rate=tax_rate,
    )