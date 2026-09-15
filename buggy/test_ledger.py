from ledger import Ledger


def test_ledgers_do_not_share_entries():
    a = Ledger()
    a.add("invoice 1", 120.0)
    b = Ledger()
    # a brand new ledger starts empty, it must not inherit a's entries
    assert b.balance() == 0.0
    b.add("refund", -30.0)
    assert a.balance() == 120.0
    assert b.balance() == -30.0
