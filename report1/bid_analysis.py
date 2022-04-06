import csv

class BidValue():
    def __init__(self, bid, value):
        self.bid = bid
        self.val = value

def print_bv(bidval):
    print(f'bid: {bidval.bid}, val: {bidval.val}')

def process_auction(auction, my_bidval):
    win_count = 0
    total_count = len(auction)
    utility_sum = 0
    for bidval in auction:
        if my_bidval.bid > bidval.bid:
            win_count += 1
            utility_sum += my_bidval.val - my_bidval.bid
    
    win_probability = round(win_count / total_count * 100, 2)
    utility_average = round(utility_sum / total_count, 2)
    return win_probability, utility_average

def process_utility(auction, my_bidval):
    total_count = len(auction)
    utility_sum = 0
    for bidval in auction:
        if my_bidval.bid > bidval.bid:
            utility_sum += my_bidval.val - my_bidval.bid
    
    utility_average = round(utility_sum / total_count, 2)
    utility_average = utility_sum / total_count
    return utility_average

def optimal_bid(auction, my_bidval):
    max_bidval = None
    max_utility_average = 0
    #for bid in range(1, 10000):
    for bidval in auction:
        bid = round(bidval.bid + 0.01, 2)
        new_bidval = BidValue(bid, my_bidval.val)
        #new_bidval = BidValue(bid/100, my_bidval.val)
        new_utility_average = process_utility(auction, new_bidval)
        if new_utility_average > max_utility_average:
            max_utility_average = round(new_utility_average, 2)
            max_bidval = new_bidval

    return max_bidval, max_utility_average


def read_input(auction_a, auction_b, rows):
    my_bidval_a = None
    my_bidval_b = None
    with open("bid_data.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if row[0] != '***5530': 
                rows.append(row)
                auction_a.append(BidValue(float(row[1]), float(row[3])))
                auction_b.append(BidValue(float(row[2]), float(row[4])))
            else:
                my_bidval_a = BidValue(float(row[1]), float(row[3]))
                my_bidval_b = BidValue(float(row[2]), float(row[4]))
    
    return my_bidval_a, my_bidval_b


def main():
    rows = []
    auction_a = []
    auction_b = []
    my_bidval_a, my_bidval_b = read_input(auction_a, auction_b, rows)
    a_winchance, a_avg_util = process_auction(auction_a, my_bidval_a)
    b_winchance, b_avg_util = process_auction(auction_b, my_bidval_b)

    max_bidval_a, max_util_avg_a = optimal_bid(auction_a, my_bidval_a)
    max_bidval_b, max_util_avg_b = optimal_bid(auction_b, my_bidval_b)

    max_a_winchance, max_util_avg_a = process_auction(auction_a, max_bidval_a)
    max_b_winchance, max_util_avg_b = process_auction(auction_b, max_bidval_b)

    print('auction a my bidval')
    print_bv(my_bidval_a)
    print('auction a maximized bidval')
    print_bv(max_bidval_a)
    print('auction b my bidval')
    print_bv(my_bidval_b)
    print('auction b maximized bidval')
    print_bv(max_bidval_b)
    print(f'auction a my bid: {my_bidval_a.bid}, value: {my_bidval_a.val}, winchance: {a_winchance}%, avg_util: {a_avg_util}')
    print(f'auction a maximized bid: {max_bidval_a.bid}, value: {max_bidval_a.val}, winchance: {max_a_winchance}%, avg_util: {max_util_avg_a}')
    print(f'auction b my bid: {my_bidval_b.bid}, value: {my_bidval_b.val}, winchance: {b_winchance}%, avg_util: {b_avg_util}')
    print(f'auction b maximized bid: {max_bidval_b.bid}, value: {max_bidval_b.val}, winchance: {max_b_winchance}%, avg_util: {max_util_avg_b}')
    x = 0
    for i in range(1000000000):
        x += i
    print(x)

main()

