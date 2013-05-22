import urllib2
import json

trades = {'btc_usd': 'https://btc-e.com/api/2/btc_usd/trades',
           'ltc_btc': 'https://btc-e.com/api/2/ltc_btc/trades',
           'ltc_usd': 'https://btc-e.com/api/2/ltc_usd/trades'}

for k, v in trades.iteritems():
    print k

    trades_feed = urllib2.urlopen(v)
    j = json.loads(trades_feed.read())
    trades_feed.close()
    print k, j

