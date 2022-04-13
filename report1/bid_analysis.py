import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class BidValue():
    def __init__(self, bid, value):
        self.bid = bid
        self.val = value

def print_bv(bidval):
    print(f'bid: {bidval.bid}, val: {bidval.val}')

def process_auction(auction, my_bidval):
    win_count = 0
    total_count = len(auction)
    for bidval in auction:
        if my_bidval.bid > bidval.bid:
            win_count += 1
    
    win_probability = win_count / total_count
    win_percentage = round(win_probability * 100, 2)
    expected_utility = round(win_probability * (my_bidval.val - my_bidval.bid), 2)
    return win_percentage, expected_utility

def process_utility(auction, my_bidval):
    win_count = 0
    total_count = len(auction)
    for bidval in auction:
        if my_bidval.bid > bidval.bid:
            win_count += 1
    win_probability = win_count / total_count
    return round(win_probability * (my_bidval.val - my_bidval.bid), 2)

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


def read_input(auction_a, auction_b, rows, netid):
    my_bidval_a = None
    my_bidval_b = None
    with open("bid_data.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if row[0] != netid: 
                rows.append(row)
                auction_a.append(BidValue(float(row[1]), float(row[3])))
                auction_b.append(BidValue(float(row[2]), float(row[4])))
            else:
                my_bidval_a = BidValue(float(row[1]), float(row[3]))
                my_bidval_b = BidValue(float(row[2]), float(row[4]))
    
    return my_bidval_a, my_bidval_b


def preprocess_auction(auction):
    #convert auctions to bid and value lists for visualizations
    auction_bid = []
    auction_val = []
    for i in auction:
        auction_bid.append(i.bid)
        auction_val.append(i.val)

    return auction_bid, auction_val

def visualize(bids, values, text_pos_x, text_pos_y, title):

    #find line of best fit
    x = np.array(values)
    y = np.array(bids)
    a, b = np.polyfit(x, y, 1)

    plt.scatter(x,y, color = 'purple')
    plt.plot(x, a*x+b, color='steelblue', linestyle='--', linewidth=2)
    plt.text(text_pos_x, text_pos_y, 'bid = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'val', size=14)
    plt.xlabel("Bidder Value, v")
    plt.ylabel("Actual Bid, b")
    plt.title(title)
    plt.show()


def analyze_netid(netid_1, netid_2):
    both_ids = [netid_1, netid_2]
    for netid in both_ids:
        rows = []
        auction_a = []
        auction_b = []
        my_bidval_a, my_bidval_b  = read_input(auction_a, auction_b, rows, netid)
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
        print('\n')
    
    #re-append my own bid and value to auctions list
    auction_a.append(my_bidval_a)
    auction_b.append(my_bidval_b)

    #preprocessing auctions for visualization 
    auction_bid_a, auction_val_a = preprocess_auction(auction_a)
    auction_bid_b, auction_val_b = preprocess_auction(auction_b)

    visualize(auction_bid_a, auction_val_a, 1, 35, "Auction A")
    visualize(auction_bid_b, auction_val_b, 55, 90, "Auction B")


def main():
    analyze_netid('***5530', '***5489')

    

main()

