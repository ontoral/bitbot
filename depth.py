import csv
from datetime import datetime
import time

import requests

UPDATE_DIVISOR = 2.0
UPDATE_COUNT = 100

urls = {'ticker': 'https://btc-e.com/api/2/{}/ticker',
        'trades': 'https://btc-e.com/api/2/{}/trades',
        'depth': 'https://btc-e.com/api/2/{}/depth'}

class BTCExchange(object):
    def __init__(self, pair):
        self.pair = pair
        self.urls = {key: value.format(pair) for (key, value) in urls.iteritems()}
        self.curr_from, self.curr_to = pair.split('_')
        self.load_trades(pair)
        #self.update_all()

    def load_ticker(self, pair):
        # For future local db support
        return []

    def load_trades(self, pair):
        # For future db support
        # Query update_divisor
        # Query update_count
        # Query (update_count) rows
        
        # For local testing, read from btc-e.com
        r = requests.get(self.urls['trades'])
        trades = r.json()

        # Set update_divisor
        self.update_divisor = UPDATE_DIVISOR

        # Set update_count
        self.update_count = UPDATE_COUNT

        # Parse and add (update_count) rows
        # Invert list to add from oldest to newest
        self.trades = [BTCTrade(trade) for trade in reversed(trades)]

        self.adjust_update()

    def adjust_update(self, new_trades_count=0):
        # Store most recent transaction ID
        self.recent_tid = self.trades[-1].tid

        # Check the update interval
        newest = datetime.fromtimestamp(self.trades[-1].date)
        oldest = datetime.fromtimestamp(self.trades[-self.update_count].date)
        self.update_interval = (newest - oldest).total_seconds() / self.update_divisor

        msg = '[{1.pair}] ==> New Trades: {0}, Recent TID: {1.recent_tid}, Next Update: {1.update_interval} s, Div: {1.update_divisor}, Count: {1.update_count}'
        print msg.format(new_trades_count, self)

    def update_all(self):
        #self.update_ticker()
        self.update_trades()
        #self.update_depth()

    def update_feed(self, feed):
        r = requests.get(self.urls['trades'])
        feed_info = r.json()
        if type(feed_info) == dict:
            if feed_info.has_key(feed):
                feed_info = feed_info[feed]
        elif type(feed_info) == list:
            feed_info = {'items': [type(feed + '_item', (object,), item) for item in feed_info]}
        setattr(self, feed, type(feed, (object,), feed_info))

    def update_trades(self):
        num_new_trades = 0
        # Parse and add new trades
        r = requests.get(self.urls['trades'])
        trades = r.json()
        feed_length = len(trades)

        # Invert list to add from oldest to newest
        for trade in reversed(trades):
            if trade['tid'] > self.recent_tid:
                self.trades.append(BTCTrade(trade))
                num_new_trades += 1

        self.adjust_update(num_new_trades)
        

class BTCTrade(object):
    """{"date":1368283934,
    "price":112.5,
    "amount":0.876452,
    "tid":3809629,
    "price_currency":"USD",
    "item":"BTC",
    "trade_type":"ask"}
    """
    def __init__(self, trade_info):
        # Convert date value to datetime object
        # trade_info['date'] = datetime.fromtimestamp(trade_info['date'])
        self.__dict__.update(trade_info)

    def __repr__(self):
        repr = '{when} {0.trade_type}: {0.amount} {0.item} -> {0.price_currency} @ {0.price}'
        return repr.format(self, when=time.strftime('%F %T', time.gmtime(self.date)))


if __name__ == '__main__':
    pairs = ['ltc_usd', 'btc_usd', 'ltc_btc']
    exchanges = [BTCExchange(pair) for pair in pairs]

    def update_exchanges():
        for exchange in exchanges:
            exchange.update_trades()

    def calc_interval():
        intervals = [exchange.update_interval for exchange in exchanges]
        return min(intervals) / 2

    def write_csv():
        for exchange in exchanges:
            num_rows = max(0, len(exchange.trades) - UPDATE_COUNT)
            with open(exchange.pair + '.csv', 'a') as f:
                csv_writer = csv.writer(f)
                for ii in range(num_rows):
                    csv_writer.writerow(exchange.trades[ii].__dict__.values())
            exchange.trades = exchange.trades[num_rows:]

    def run_it():
        while True:
            update_exchanges()
            write_csv()
            interval = calc_interval()
            print 'Sleeping {} minutes...'.format(interval / 60)
            time.sleep(interval)

