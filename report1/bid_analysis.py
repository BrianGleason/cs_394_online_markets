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


def read_netids():
    with open("bid_data.csv", 'r') as file:
        netids=[]
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            netids.append(row[0])
    
    return netids

def preprocess_auction(auction):
    #convert auctions to bid and value lists for visualizations
    auction_bid = []
    auction_val = []
    for i in auction:
        auction_bid.append(i.bid)
        auction_val.append(i.val)

    return auction_bid, auction_val

def visualize(bids_1, values_1, bids_2, values_2):

    #find line of best fit
    x = np.array(values_1 + values_2)
    y = np.array(bids_1 + bids_2)
    a, b = np.polyfit(x, y, 1)

    plt.scatter(values_1,bids_1, color = 'purple')
    plt.scatter(values_2,bids_2, color = 'red')
    plt.plot(x, a*x+b, color='steelblue', linestyle='--', linewidth=2)
    plt.text(1, 65, 'bid = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'val', size=14)
    plt.xlabel("Bidder Value, v")
    plt.ylabel("Actual Bid, b")
    plt.title("Bidder Value vs. Actual Bids (Auction A and Auction B)")
    plt.legend(["Auction A" , "Auction B"])
    
    plt.savefig('val_vid_scatterplot.png')

    plt.show()

def perc_calc(bids, values):

    count = 0
    total_perc = 0
    for i in range(len(bids)):
        if bids[i] == values[i] / 2:
            count += 1
        total_perc += (bids[i] / values[i]) 

    equil_perc = (count / len(bids)) * 100

    avg_perc = (total_perc / len(bids)) * 100

    return round(equil_perc, 2), round(avg_perc, 2)


def analyze_netid(netids):
    sum_optimal_bid_percentages_a = 0
    sum_optimal_bid_percentages_b = 0

    for netid in netids:
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

        if len(netids) < 5:
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

        #find optimal bids
        current_auction_a_opt_bid = max_bidval_a.bid / max_bidval_a.val * 100
        current_auction_b_opt_bid = max_bidval_b.bid / max_bidval_b.val * 100
        sum_optimal_bid_percentages_a += current_auction_a_opt_bid
        sum_optimal_bid_percentages_b += current_auction_b_opt_bid
    
    #re-append my own bid and value to auctions list
    auction_a.append(my_bidval_a)
    auction_b.append(my_bidval_b)

    #preprocessing auctions for visualization 
    auction_bid_a, auction_val_a = preprocess_auction(auction_a)
    auction_bid_b, auction_val_b = preprocess_auction(auction_b)

    #combine vids and values from both auctions

    total_bids = auction_bid_a + auction_bid_b

    total_values = auction_val_a + auction_val_b

    #Calculate what percent found the Bayes-Nash equilibrium and average percent of total value 

    equil_perc = perc_calc(total_bids, total_values)[0]
    a_equil_perc = perc_calc(auction_bid_a, auction_val_a)[0]
    b_equil_perc = perc_calc(auction_bid_b, auction_val_b)[0]

    avg_perc = perc_calc(total_bids, total_values)[1]
    a_avg_perc = perc_calc(auction_bid_a, auction_val_a)[1]
    b_avg_perc = perc_calc(auction_bid_b, auction_val_b)[1]
    if len(netids) < 5:
        print(f'Percent of bids that are Bayes-Nash Equilibrium: {equil_perc}%')
        print(f'Percent of bids that are Bayes-Nash Equilibrium from Auction A: {a_equil_perc}%')
        print(f'Percent of bids that are Bayes-Nash Equilibrium from Auction B: {b_equil_perc}%')
        print(f'Average percent of total value: {avg_perc}%')
        print(f'Average percent of total value from Auction A: {a_avg_perc}%')
        print(f'Average percent of total value from Auction B: {b_avg_perc}%')


    #visualize scatterplot
    if len(netids) < 5:
        visualize(auction_bid_a, auction_val_a, auction_bid_b, auction_val_b)

        total_bids = len(netids)
        print("Average optimal bid percentage auction A", sum_optimal_bid_percentages_a / total_bids)
        print("Average optimal bid percentage auction B", sum_optimal_bid_percentages_b / total_bids)

    #return average optimal bid percentage
    return
  

def main():
    our_netids = ['***5530', '***5489']
    analyze_netid(our_netids)
    all_netids = read_netids()
    analyze_netid(all_netids)

    

main()

