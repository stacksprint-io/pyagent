"""Prints a customer receipt. Line amounts and the total are shown in
whole cents, converted from the float prices the store API returns."""


def to_cents(price):
    return int(price * 100)


def receipt_total_cents(items):
    """items: list of (unit_price, quantity). Returns the total in cents."""
    total = 0
    for unit_price, quantity in items:
        total += to_cents(unit_price) * quantity
    return total
