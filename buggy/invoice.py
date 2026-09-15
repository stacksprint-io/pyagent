"""Order billing for the storefront. Totals are rounded to cents."""


def invoice_total(items, discount_rate):
    """items: list of (unit_price, quantity). Discount applies to the
    whole order, then the final amount is rounded to cents."""
    total = 0.0
    for unit_price, quantity in items:
        total += round(unit_price * quantity * (1 - discount_rate), 2)
    return round(total, 2)
