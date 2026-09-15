from invoice import invoice_total


def test_discount_applies_to_the_order_not_per_line():
    items = [(19.99, 3), (4.35, 2), (0.89, 5)]
    # subtotal is 73.12, minus 15 percent = 62.152, rounded to 62.15
    assert invoice_total(items, 0.15) == 62.15


def test_no_discount():
    assert invoice_total([(10.00, 2)], 0.0) == 20.00
