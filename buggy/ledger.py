"""A tiny running ledger. Each Ledger starts empty and tracks its own
entries; balance() folds them in order."""


class Ledger:
    def __init__(self, entries=[]):
        self.entries = entries

    def add(self, label, amount):
        self.entries.append((label, amount))

    def balance(self):
        total = 0.0
        for _, amount in self.entries:
            total += amount
        return round(total, 2)
