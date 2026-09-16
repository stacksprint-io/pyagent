from receipt import receipt_total_cents


def test_receipt_total_matches_the_posted_prices():
    items = [(19.99, 3), (4.35, 2), (0.89, 5)]
    # 3x 1999 + 2x 435 + 5x 89 = 7312 cents, straight off the price tags
    assert receipt_total_cents(items) == 7312
