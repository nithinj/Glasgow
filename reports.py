
import sys


DELIMITER = ','
BUY = 'B'
SELL = 'S'
MAX_ENTITY_NAME = 20


class Transaction(object):
    """
    Used to read raw transaction detail and process it for required information
    we are interested in. Note, this does not store all the details of a
    transaction. It is also assumed that input data is in certain specific
    order separated by delimiter and having '8' columns.
    """

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
    """
    Generic class for both daily and ranking reports
    """

    def initialize(self):
        self.outgoing = 0.0
        self.incoming = 0.0

    def __init__(self, transact):
        self.initialize()
        self.update(transact)

    def update(self, transact):
        """
        Adds new transaction amount to the
        incoming/outgoing value based on the type.
        """
        if transact.type == BUY:
            self.outgoing += transact.USD_amount
        elif transact.type == SELL:
            self.incoming += transact.USD_amount


def daily_transaction_report(trans_dict):
    """ Generates daily transaction report from trans_dict """
    print("\n\t\tDAILY TRANSACTION REPORT")
    print('=' * (MAX_ENTITY_NAME + 30))
    print("DATE\t\tINCOMING\tOUTGOING")
    "Price: $ %8.2f" % (356.08977)
    for date, settle in trans_dict.items():
        print("%s\t$ %12.2f\t$ %12.2f" %
              (date, settle.incoming, settle.outgoing))


def entity_ranking_report(trans_dict, type):
    """
    Generates entity ranking report from trans_dict.
    attr of type can be "incoming" / "outgoing"
    """
    print("\n\n\t\tENTITY RANKING REPORT - " + type.upper())
    print('=' * (MAX_ENTITY_NAME + 30))
    print("RANK\tENTITY\t\t\t" + type.upper())
    rank = 1
    if type == "incoming":
        for entity in sorted(trans_dict, key=lambda name:
                             trans_dict[name].incoming, reverse=True):
            if trans_dict[entity].incoming == 0:
                break
            print("%5d\t%s\t$ %15.2f" % (rank, entity[:MAX_ENTITY_NAME].ljust(
                MAX_ENTITY_NAME), trans_dict[entity].incoming))
            rank += 1
    elif type == "outgoing":
        for entity in sorted(trans_dict, key=lambda name:
                             trans_dict[name].outgoing, reverse=True):
            if trans_dict[entity].outgoing == 0:
                break
            print("%5d\t%s\t$ %15.2f" % (rank, entity[:MAX_ENTITY_NAME].ljust(
                MAX_ENTITY_NAME), trans_dict[entity].outgoing))
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
