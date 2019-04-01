
import sys


DELIMITER = ','
BUY = 'B'
SELL = 'S'
MAX_ENTITY_NAME = 20


class Transaction(object):

    def __init__(self, row):
        row = row.split(DELIMITER)
        self.entity = row[0].strip()
        self.type = row[1].strip()
        agreed_fx = float(row[2].strip())
        self.settlement_date = row[5].strip()
        units = float(row[6].strip())
        price_per_unit = float(row[7].strip())
        self.USD_amount = price_per_unit * units * agreed_fx


class Amount_Settled(object):

    def initialize(self):
        self.outgoing = 0.0
        self.incoming = 0.0

    def __init__(self, transact):
        self.initialize()
        self.update(transact)

    def update(self, transact):
        if transact.type == BUY:
            self.outgoing += transact.USD_amount
        elif transact.type == SELL:
            self.incoming += transact.USD_amount


def daily_transaction_report(trans):
    print("\n\t\tDAILY TRANSACTION REPORT")
    print('=' * (MAX_ENTITY_NAME + 30))
    print("DATE\t\tINCOMING\tOUTGOING")
    "Price: $ %8.2f" % (356.08977)
    for date, settle in trans.items():
        print("%s\t$ %12.2f\t$ %12.2f" %
              (date, settle.incoming, settle.outgoing))


def entity_ranking_report(trans, type):
    print("\n\n\t\tENTITY RANKING REPORT - " + type.upper())
    print('=' * (MAX_ENTITY_NAME + 30))
    print("RANK\tENTITY\t\t\t" + type.upper())
    rank = 1
    if type == "incoming":
        for entity in sorted(trans, key=lambda name: trans[name].incoming, reverse=True):
            if trans[entity].incoming == 0:
                break
            print("%5d\t%s\t$ %15.2f" % (rank, entity[:MAX_ENTITY_NAME].ljust(
                MAX_ENTITY_NAME), trans[entity].incoming))
            rank += 1
    elif type == "outgoing":
        for entity in sorted(trans, key=lambda name: trans[name].outgoing, reverse=True):
            if trans[entity].outgoing == 0:
                break
            print("%5d\t%s\t$ %15.2f" % (rank, entity[:MAX_ENTITY_NAME].ljust(
                MAX_ENTITY_NAME), trans[entity].outgoing))
            rank += 1


if __name__ == "__main__":
    daily_trans = {}
    entity_trans = {}

    for line in sys.stdin:
        transact = Transaction(line)
        if transact.settlement_date in daily_trans:
            daily_trans[transact.settlement_date].update(transact)
        else:
            daily_trans[transact.settlement_date] = Amount_Settled(transact)

        if transact.entity in entity_trans:
            entity_trans[transact.entity].update(transact)
        else:
            entity_trans[transact.entity] = Amount_Settled(transact)

    daily_transaction_report(daily_trans)
    entity_ranking_report(entity_trans, "incoming")
    entity_ranking_report(entity_trans, "outgoing")
